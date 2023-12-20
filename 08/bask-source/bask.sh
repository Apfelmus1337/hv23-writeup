#!/usr/bin/bash

####################################
#        BASK v0.0.1 Alpha
#        Webserver in Bash
####################################

# Create the response FIFO
rm -f response
mkfifo response

function handleRequest() {
  ## Read request, parse each line and breaks until empty line
  while read -r line; do
    echo "$line"
    # Remove newline characters
    trline=$(echo "$line" | tr -d '[\r\n]')

    # No more lines? Break!
    [ -z "$trline" ] && break

    # Parse first line
    HEADLINE_REGEX='(.*?)\s(.*?)\sHTTP.*?'
    [[ "$trline" =~ $HEADLINE_REGEX ]] &&
      REQUEST=$(echo "$trline" | sed -E "s/$HEADLINE_REGEX/\1 \2/")

    # Parse content length -> body data
    CONTENT_LENGTH_REGEX='Content-Length:\s(.*?)'
    [[ "$trline" =~ $CONTENT_LENGTH_REGEX ]] &&
        CONTENT_LENGTH=$(echo "$trline" | sed -E "s/$CONTENT_LENGTH_REGEX/\1/")

    # Parse cookies for admin auth
    COOKIE_REGEX='Cookie:\s(.*?)=(.*?)'
    [[ "$trline" =~ $COOKIE_REGEX ]] &&
    COOKIES=$(echo "$trline" | sed -E "s/$COOKIE_REGEX/\1=\2/")


  done
    # Read body data on POST
    if [ -n "$CONTENT_LENGTH" ]; then
      BODY_REGEX='(.*?)=(.*?)'

      # Read the remaining request body
      while read -r -n "$CONTENT_LENGTH" -t1 body; do
        echo "$body"
        INPUT_VALUE=$(echo "$body" | sed -E "s/$BODY_REGEX/\2/")
      done
    fi


# Default code
STATUS_CODE=200
# Route to the response handler based on the REQUEST match
  case "$REQUEST" in
    ### Static files
    "GET /files/styles.css" )
        ADDITIONAL_HEADERS="Content-Type: text/css"
        RESPONSE=$(cat files/styles.css) ;;
    ### Routes
    "GET /")
        RESPONSE=$(bash templates/index.sh) ;;
    "GET /login")
        RESPONSE=$(bash templates/get_login.sh) ;;
    "POST /login")
        RESPONSE=$(POST_PASSWORD=$INPUT_VALUE bash templates/post_login.sh) ;;
    "GET /admin")
        RESPONSE=$(COOKIES=$COOKIES bash templates/admin.sh) ;;
    ### Default (404)
    *)
        STATUS_CODE=404
        RESPONSE=$(bash templates/404.sh) ;;
  esac

  echo -e "HTTP/1.1 $STATUS_CODE OK\r\nContent-Length: ${#RESPONSE}\r\n$ADDITIONAL_HEADERS\r\n\r\n$RESPONSE" > response
}

echo 'Listening on 0.0.0.0:3000...'

# Serve requests
while true; do
cat response | nc -lN 3000 | handleRequest
done



##############################################################################
# CREDITS
#
# Web Template:
# https://getbootstrap.com/docs/4.1/examples/cover/
#
# Webserver in bash:
# https://dev.to/leandronsp/building-a-web-server-in-bash-part-i-sockets-2n8b
##############################################################################

#!/bin/bash

# Include header
bash templates/header.sh

# We only have one cookie so first value should be admin password
FIRST_COOKIE=$(cut -d "=" -f 2 <<< "$COOKIES")

# Check if admin password is valid
if [[ "$FIRST_COOKIE" == "$ADMIN_PASSWORD" ]]; then
    cat << EOF
    <main role="main" class="inner cover">
        <h1 class="cover-heading">Admin Panel</h1>
        <p>Your flag is: $FLAG</p>
    </main>
EOF
else
    cat << EOF
    <main role="main" class="inner cover">
        <p>You are not authorized to view this page.</p>
        <script>
            document.cookie = "";
            setTimeout(function() {
                window.location.href = "/login";
            }, 2000);
        </script>
    </main>
EOF
fi
# Include footer
bash templates/footer.sh

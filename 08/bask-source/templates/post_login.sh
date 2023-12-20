#!/bin/bash

# Include header
bash templates/header.sh

cat << EOF
<main role="main" class="inner cover">
    <h1>Login</h1>
EOF

if [[ $ADMIN_PASSWORD == $POST_PASSWORD ]]; then
    cat << EOF
    <div class="alert alert-success" role="alert">
        <strong>Successfully logged in, redirecting...</strong>
    </div>
    <script>
        document.cookie = "admin_token=$POST_PASSWORD;path=/";
        setTimeout(function () {
            window.location.href = "/admin";
        }, 2000);
    </script>
EOF
else
    cat << EOF

    <div class="alert alert-danger" role="alert">
        <strong>Invalid username or password!</strong>
    </div>
EOF


fi

cat << EOF
</main>
EOF

# Include footer
bash templates/footer.sh

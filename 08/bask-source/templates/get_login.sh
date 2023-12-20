#!/bin/bash

# Include header
bash templates/header.sh
cat << EOF
<main role="main" class="inner cover">
    <h1>Login</h1>
    <p class="lead">Please enter your password to enter the admin section.</p>
    <form method="POST">
    <div class="col-auto">
        <input name="password" type="password" placeholder="Password" class="form-control mb-2" id="password" required>
        <button type="submit" class="btn btn-primary mb-2">Login</button>
    </div>
    </form>
</main>
EOF
# Include footer
bash templates/footer.sh

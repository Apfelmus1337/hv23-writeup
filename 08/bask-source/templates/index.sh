#!/bin/bash

# Include header
bash templates/header.sh
cat << EOF
<script>
const jsConfetti = new JSConfetti();
jsConfetti.addConfetti({
   emojis: ['*️'],
   confettiColors: ['#ffffff'],
   emojiSize: 30,
});
</script>
<main role="main" class="inner cover">
    <h1>🎅 Santa<b>Labs</b> bask</h1>
    <p class="lead">Ditch flask and complicated python. With <b>bask</b>, you can write interactive websites using good, old bash and even template your files by using dynamic scripting!</p>
</main>
EOF
# Include footer
bash templates/footer.sh

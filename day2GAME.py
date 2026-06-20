import random

secret = random.randint(1, 100)
lives = 7

print("🔮 The Oracle has chosen a number between 1 and 100.")
print(f"You have {lives} lives. Guess wisely...")

while lives > 0:
    guess = int(input("Your guess: "))
    if guess == secret:
        print(f"✨ YES! The Oracle is impressed! Lives remaining: {lives}")
        break
    elif guess < secret:
        print("📈 Higher!")
    else:
        print("📉 Lower!")
    lives = lives - 1
    print(f"Lives left: {lives} 💀")

if lives == 0:
    print(f"💀 Game Over! The number was {secret}.")

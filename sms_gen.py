import os
import time
import random
import pyfiglet
import colorama
import phonenumbers
from termcolor import colored

# Initialize colorama
colorama.init()

# Define phone number formats for each country
phone_formats = {
    'USA': '+1##########',
    'CANADA': '+1##########',
    'AFGHANISTAN': '+93#########',
    # Add more countries and their phone number formats as needed
}

def print_banner():
    # Function to print the banner text
    custom_fig = pyfiglet.Figlet(font='small', width=180)
    banner_text = custom_fig.renderText('\tSMS GEN')
    banner = colored(banner_text, 'green', 'on_black', ['bold'])
    print(banner)
    
    # Print sub-banner with link
    sub_banner_text = "https://discord.gg/portlords\n"
    sub_banner = colored(sub_banner_text, 'green')
    print(sub_banner)

def generate_phone_numbers(country, num_numbers):
    # Function to generate random phone numbers for the given country
    if country not in phone_formats:
        print("Invalid country selected.")
        return

    phone_numbers = []
    template = phone_formats[country].replace('#', '{}')

    for _ in range(num_numbers):
        # Generate random digits and format as per the country's template
        digits = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        phone_number = template.format(*digits)
        phone_numbers.append(phone_number)

    # Save generated phone numbers to a file
    save_to_file('generated.txt', phone_numbers)
    print(f"Generated and saved {num_numbers} phone numbers to generated.txt")

def validate_phone_numbers(phone_numbers):
    # Function to validate the generated phone numbers
    valid_count, invalid_count = 0, 0

    def parse_and_check_number(number):
        # Nested function to parse and validate each phone number
        nonlocal valid_count, invalid_count
        try:
            parsed_number = phonenumbers.parse(number)
            if phonenumbers.is_valid_number(parsed_number):
                valid_count += 1
            else:
                invalid_count += 1
        except phonenumbers.phonenumberutil.NumberParseException:
            invalid_count += 1

    # Iterate through the list of phone numbers and validate each one
    for number in phone_numbers:
        parse_and_check_number(number)

    # Save valid and invalid phone numbers to separate files
    save_to_file('valid.txt', [number for number in phone_numbers if parse_and_check_number(number)[0]])
    save_to_file('invalid.txt', [number for number in phone_numbers if parse_and_check_number(number)[1]])
    print(f"Valid: {valid_count}, Invalid: {invalid_count}")

def save_to_file(filename, lines):
    # Function to save data to a file
    with open(filename, 'w') as outfile:
        outfile.writelines(['\n'.join(lines), '\n'])

os.system('cls')  # Clear the console screen

def main():
    # Main function to drive the SMS generator tool
    print_banner()

    # Get user input for country name or code and number of phone numbers to generate
    print("Supports all 191 countries.\n")
    country_input = input(colored("Please enter a country name (in capital letters): ", "green", "on_black"))
    if country_input not in phone_formats:
        # If the input is not in the predefined formats, try to match it with a country or code
        for c, n in phone_formats.items():
            if country_input.lower() in [c.lower(), n[1:]]:
                country = c
                break
        else:
            print("Invalid country name")
            return
    else:
        country = country_input

    num_numbers = int(input(colored("Number of phones to generate: ", "green", "on_black")))

    # Generate specified number of phone numbers for the selected country
    generate_phone_numbers(country, num_numbers)

    # Validate the generated phone numbers
    validate = input(colored("Validate the generated phone numbers? (Y/N) ", "green", "on_black")).lower()
    if validate == 'y':
        validate_phone_numbers(get_generated_phone_numbers())
    elif validate == 'n':
        print("Program exiting...")
    else:
        print("Invalid input. Program exiting...")

main()

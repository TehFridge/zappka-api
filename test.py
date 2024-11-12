# This script has no error handlers or anything like that. Purely for testing purposes.
# Overall this script is a mess.
import zappka
import qrcode # Print QR code to console

# Get token needed for phone authorization
idToken = zappka.auth.get_idToken()

# Get info from user
phone_number = input("Enter phone number (ex. 123456789): ")
country_code = input("Enter country code (ex. 48): ")

print("Sending SMS authentication request.")

# Send phone authorization request. Sends a message to given phone number.
zappka.auth.send_verification_code(idToken, country_code, phone_number)

print("You should receive a message with a verification code.")

# Get code from user
sms_code = input("Enter received SMS code: ")

customToken = zappka.auth.phone_auth(idToken, country_code, phone_number, sms_code)

identityProviderToken = zappka.auth.verify_custom_token(customToken)

# Required so the API won't cry about not starting a session or something.
zappka.auth.get_account_info(identityProviderToken)

snrsToken = identityProviderToken

while True:
    print("\n")
    print("Main")
    print("1. Superlogin")
    print("2. Synerise")
    print("3. QR")
    print("4. Exit")
    choice = int(input("> "))

    match choice:
        case 1:
            while True:
                print("\n")
                print("Main > Superlogin")
                print("1. Change first name.")
                print("2. Change email.")
                print("3. Change birth date (YYYY-MM-DD).")
                print("4. Get account details")
                print("5. Exit.")

                choice = int(input("> "))

                match choice:
                    case 1:
                        try:
                            value = input("Enter name: ")
                            zappka.superlogin.change_details(identityProviderToken, "firstName", value)
                        except KeyboardInterrupt:
                            pass
                    case 2:
                        try:
                            value = input("Enter email: ")
                            zappka.superlogin.change_details(identityProviderToken, "email", value)
                        except KeyboardInterrupt:
                            pass
                    case 3:
                        try:
                            value = input("Enter birth date (YYYY-MM-DD): ")
                            zappka.superlogin.change_details(identityProviderToken, "birthDate", value)
                        except KeyboardInterrupt:
                            pass
                    case 4:
                        print(zappka.superlogin.get_details(identityProviderToken))
                    case 5:
                        break
                    case _:
                        print("?")
        case 2:
            while True:
                print("\n")
                print("Main > Synerise")
                print("1. Get żappsy amount")
                print("2. Transfer żappsy (NOT WORKING - API CHANGES)")
                print("3. Get personal information")
                print("4. Get żappsy history (NOT WORKING - API CHANGES)")
                print("5. Coupon functions (NOT WORKING - Workin on it i swear)")
                print("6. Exit")

                choice = int(input("> "))

                match choice:
                    case 1:
                        print(f"Current żappsy amount: {zappka.snrs.get_current_zappsy_amount(snrsToken)}")
                        #print(f"All-time collected żappsy amount: {zappka.snrs.get_alltime_zappsy_amount(snrsToken)}")
                    case 2:
                        try:
                            phoneNumber = input("Enter recipient phone number (ex. 123456789): ")
                            amount = int(input("Enter amount of żappsy: "))
                            message = input("Enter message: ")
                            anonymous = input("Anonymous (replace first name)? [Y/N/C, default: Y]: ")
                            match anonymous:
                                case "Y":
                                    firstName = "Anonimowy"
                                case "N":
                                    firstName = zappka.snrs.get_personal_information(snrsToken)['firstName']
                                case "C":
                                    break
                                case _:
                                    firstName = "Anonimowy"

                            zappka.snrs.transfer_zappsy(snrsToken, phoneNumber, amount, message, firstName)
                        except KeyboardInterrupt:
                            pass
                    case 3:
                        print(zappka.snrs.get_personal_information(snrsToken))
                    case 4:
                        print(zappka.snrs.get_zappsy_history(snrsToken))
                    case 5:
                        while True:
                            print("\n")
                            print("Main > Synerise > Coupons")
                            print("1. Get offer settings")
                            print("2. Get top offers")
                            print("3. Exit")

                            choice = int(input("> "))

                            match choice:
                                case 1:
                                    print(zappka.snrs.coupons.get_offer_settings(snrsToken))
                                case 2:
                                    print(zappka.snrs.coupons.get_top_offers(snrsToken))
                                case 3:
                                    break
                                case _:
                                    print("?")
                    case 6:
                        break
                    case _:
                        print("?")
        case 3:
            while True:
                print("1. Show QR code")
                print("2. Exit")

                choice = int(input("> "))

                match choice:
                    case 1:
                        url = zappka.qr.get_qr_code(identityProviderToken)

                        # Show URL as QR code
                        qr = qrcode.QRCode(
                                version=1,
                                error_correction=qrcode.constants.ERROR_CORRECT_H,
                                box_size=10,
                                border=4,
                        )
                        qr.add_data(url)
                        qr.print_ascii(invert=True)

                        print(url)
                    case 2:
                        break
                    case _:
                        print("?")
        case 4:
            exit()

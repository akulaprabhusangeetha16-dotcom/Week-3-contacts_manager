# ============================================
# TEST FILE FOR CONTACT MANAGEMENT SYSTEM
# (MATCHES ORIGINAL FUNCTION NAMES)
# ============================================

import contacts_manager

def test_check_phone():
    print("\n--- Phone Check Test ---")
    print(contacts_manager.check_phone("7981393388"))     # valid
    print(contacts_manager.check_phone("667788993300"))   # valid
    print(contacts_manager.check_phone("12345"))          # invalid

def test_check_email():
    print("\n--- Email Check Test ---")
    print(contacts_manager.check_email("123@gmail.com"))  # valid
    print(contacts_manager.check_email("134@gmail.com"))  # valid
    print(contacts_manager.check_email("wrongemail"))     # invalid

def test_load_data():
    print("\n--- Load Data Test ---")
    contacts = contacts_manager.load_data()
    print("Loaded contacts:", list(contacts.keys()))

def test_find_contacts():
    print("\n--- Find Contacts Test ---")
    contacts = contacts_manager.load_data()
    results = contacts_manager.find_contacts(contacts, "a")
    for name in results:
        print("Found:", name)

if __name__ == "__main__":
    test_check_phone()
    test_check_email()
    test_load_data()
    test_find_contacts()

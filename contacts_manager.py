# Contact Management System
# Week 3 Project - Functions & Dictionaries

import json
import re
from datetime import datetime, timedelta
import csv
import os

# File to store contacts
DATA_FILE = 'contacts_data.json'

def check_phone(phone):
    """Check phone number format"""
    # Strip non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Allow 10-15 digits for international
    if 10 <= len(digits_only) <= 15:
        return True, digits_only
    return False, None

def check_email(email):
    """Check email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def create_contact(contacts):
    """Create a new contact entry"""
    print("\n--- ADD NEW CONTACT ---")
    
    # Prompt for name
    while True:
        name = input("Enter contact name: ").strip()
        if name:
            if name in contacts:
                print(f"Contact '{name}' already exists!")
                choice = input("Do you want to update instead? (y/n): ").lower()
                if choice == 'y':
                    modify_contact(contacts, name)
                    return contacts
            break
        print("Name cannot be empty!")
    
    # Prompt for phone with check
    while True:
        phone = input("Enter phone number: ").strip()
        is_valid, cleaned_phone = check_phone(phone)
        if is_valid:
            break
        print("Invalid phone number! Please enter 10-15 digits.")
    
    # Prompt for email with check
    while True:
        email = input("Enter email (optional, press Enter to skip): ").strip()
        if not email or check_email(email):
            break
        print("Invalid email format!")
    
    # Prompt for other details
    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family/Other): ").strip() or "Other"
    
    # Add to contacts dict
    contacts[name] = {
        'phone': cleaned_phone,
        'email': email if email else None,
        'address': address if address else None,
        'group': group,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    print(f"✅ Contact '{name}' added successfully!")
    return contacts

def find_contacts(contacts, query):
    """Find contacts by name (partial match)"""
    query_lower = query.lower()
    matches = {}
    
    for name, details in contacts.items():
        if query_lower in name.lower():
            matches[name] = details
    
    return matches

def show_results(matches):
    """Show search results in formatted way"""
    if not matches:
        print("No contacts found.")
        return
    
    print(f"\nFound {len(matches)} contact(s):")
    print("-" * 50)
    
    for i, (name, details) in enumerate(matches.items(), 1):
        print(f"{i}. {name}")
        print(f"   📞 Phone: {details['phone']}")
        if details['email']:
            print(f"   📧 Email: {details['email']}")
        if details['address']:
            print(f"   📍 Address: {details['address']}")
        print(f"   👥 Group: {details['group']}")
        print()

def modify_contact(contacts, name=None):
    """Modify an existing contact"""
    if not name:
        name = input("Enter contact name to update: ").strip()
    
    if name not in contacts:
        print(f"Contact '{name}' not found!")
        return contacts
    
    print(f"\n--- UPDATE CONTACT: {name} ---")
    
    # Update phone
    current_phone = contacts[name]['phone']
    new_phone = input(f"Enter new phone (current: {current_phone}, press Enter to skip): ").strip()
    if new_phone:
        is_valid, cleaned_phone = check_phone(new_phone)
        if is_valid:
            contacts[name]['phone'] = cleaned_phone
        else:
            print("Invalid phone, keeping current.")
    
    # Update email
    current_email = contacts[name]['email'] or "None"
    new_email = input(f"Enter new email (current: {current_email}, press Enter to skip): ").strip()
    if new_email:
        if check_email(new_email):
            contacts[name]['email'] = new_email
        else:
            print("Invalid email, keeping current.")
    
    # Update address
    current_address = contacts[name]['address'] or "None"
    new_address = input(f"Enter new address (current: {current_address}, press Enter to skip): ").strip()
    if new_address:
        contacts[name]['address'] = new_address
    
    # Update group
    current_group = contacts[name]['group']
    new_group = input(f"Enter new group (current: {current_group}, press Enter to skip): ").strip()
    if new_group:
        contacts[name]['group'] = new_group
    
    contacts[name]['updated_at'] = datetime.now().isoformat()
    print(f"✅ Contact '{name}' updated successfully!")
    return contacts

def remove_contact(contacts):
    """Remove a contact"""
    name = input("Enter contact name to delete: ").strip()
    
    if name not in contacts:
        print(f"Contact '{name}' not found!")
        return contacts
    
    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
    if confirm == 'y':
        del contacts[name]
        print(f"✅ Contact '{name}' deleted successfully!")
    else:
        print("Deletion cancelled.")
    
    return contacts

def show_all_contacts(contacts):
    """Show all contacts"""
    if not contacts:
        print("No contacts to display.")
        return
    
    print(f"\n--- ALL CONTACTS ({len(contacts)} total) ---")
    print("=" * 60)
    
    for name, details in sorted(contacts.items()):
        print(f"👤 {name}")
        print(f"   📞 {details['phone']}")
        if details['email']:
            print(f"   📧 {details['email']}")
        if details['address']:
            print(f"   📍 {details['address']}")
        print(f"   👥 {details['group']}")
        print("-" * 40)

def export_csv(contacts):
    """Export contacts to CSV"""
    if not contacts:
        print("No contacts to export.")
        return
    
    filename = input("Enter CSV filename (default: contacts_export.csv): ").strip() or "contacts_export.csv"
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Phone', 'Email', 'Address', 'Group', 'Created At', 'Updated At'])
            for name, details in sorted(contacts.items()):
                writer.writerow([
                    name,
                    details['phone'],
                    details['email'] or '',
                    details['address'] or '',
                    details['group'],
                    details['created_at'],
                    details['updated_at']
                ])
        print(f"✅ Contacts exported to {filename}")
    except Exception as e:
        print(f"Error exporting: {e}")

def show_stats(contacts):
    """Show contact statistics"""
    total = len(contacts)
    groups = {}
    recent = 0
    week_ago = datetime.now() - timedelta(days=7)
    
    for details in contacts.values():
        group = details['group']
        groups[group] = groups.get(group, 0) + 1
        
        updated = datetime.fromisoformat(details['updated_at'])
        if updated > week_ago:
            recent += 1
    
    print("\n--- CONTACT STATISTICS ---")
    print(f"Total Contacts: {total}")
    print("\nContacts by Group:")
    for group, count in groups.items():
        print(f"  {group}: {count} contact(s)")
    print(f"\nRecently Updated (last 7 days): {recent}")

def load_data():
    """Load contacts from file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error reading contacts file. Starting fresh.")
    else:
        print("✅ No existing contacts file found. Starting fresh.")
    return {}

def save_data(contacts):
    """Save contacts to file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(contacts, f, indent=4)
        print("✅ Contacts saved to contacts_data.json")
    except Exception as e:
        print(f"Error saving: {e}")

def main():
    """Main program loop"""
    contacts = load_data()
    
    while True:
        print("\n" + "=" * 50)
        print("      CONTACT MANAGEMENT SYSTEM")
        print("=" * 50)
        print("\n==============================")
        print("          MAIN MENU")
        print("==============================")
        print("1. Add New Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. View All Contacts")
        print("6. Export to CSV")
        print("7. View Statistics")
        print("8. Exit")
        print("==============================")
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            contacts = create_contact(contacts)
            save_data(contacts)
        elif choice == '2':
            query = input("Enter name to search: ").strip()
            results = find_contacts(contacts, query)
            show_results(results)
        elif choice == '3':
            contacts = modify_contact(contacts)
            save_data(contacts)
        elif choice == '4':
            contacts = remove_contact(contacts)
            save_data(contacts)
        elif choice == '5':
            show_all_contacts(contacts)
        elif choice == '6':
            export_csv(contacts)
        elif choice == '7':
            show_stats(contacts)
        elif choice == '8':
            save_data(contacts)
            print("\n" + "=" * 50)
            print("Thank you for using Contact Management System!")
            print("=" * 50)
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
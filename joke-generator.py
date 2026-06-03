#!/usr/bin/env python3
"""
Random Joke Generator
Fetches jokes from the Official Joke API and displays them in the terminal.
"""

import requests
import json
from typing import Optional, Dict, Any
import sys


class JokeGenerator:
    """A simple joke generator that uses the Official Joke API."""
    
    BASE_URL = "https://official-joke-api.appspot.com"
    
    def __init__(self):
        """Initialize the JokeGenerator with the API base URL."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JokeGenerator/1.0'
        })
    
    def get_random_joke(self) -> Optional[Dict[str, Any]]:
        """
        Fetch a random joke from the API.
        
        Returns:
            dict: Joke data with 'type', 'setup', and 'punchline' keys.
            None: If the request fails.
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/random_joke", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching joke: {e}", file=sys.stderr)
            return None
    
    def get_joke_by_type(self, joke_type: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a random joke of a specific type.
        
        Args:
            joke_type: Type of joke ('general', 'knock-knock', 'programming')
        
        Returns:
            dict: Joke data with 'type', 'setup', and 'punchline' keys.
            None: If the request fails.
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/jokes/{joke_type}/random",
                timeout=5
            )
            response.raise_for_status()
            return response.json()[0]  # API returns a list
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {joke_type} joke: {e}", file=sys.stderr)
            return None
        except (IndexError, KeyError) as e:
            print(f"❌ Invalid joke type: '{joke_type}'", file=sys.stderr)
            return None
    
    def get_available_types(self) -> Optional[list]:
        """
        Get list of available joke types.
        
        Returns:
            list: Available joke types.
            None: If the request fails.
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/types", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching joke types: {e}", file=sys.stderr)
            return None
    
    def display_joke(self, joke: Dict[str, Any]) -> None:
        """
        Display a joke in a formatted way.
        
        Args:
            joke: Dictionary containing 'setup' and 'punchline' keys.
        """
        if not joke:
            return
        
        print("\n" + "=" * 60)
        print(f"📝 {joke.get('setup', 'Setup not found')}")
        print("-" * 60)
        print(f"😂 {joke.get('punchline', 'Punchline not found')}")
        print("=" * 60 + "\n")


def main():
    """Main function to demonstrate the joke generator."""
    generator = JokeGenerator()
    
    print("\n🤣 Welcome to the Random Joke Generator! 🤣\n")
    
    while True:
        print("Options:")
        print("1. Get a random joke")
        print("2. Get a specific type of joke")
        print("3. See available joke types")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n⏳ Fetching a random joke...")
            joke = generator.get_random_joke()
            generator.display_joke(joke)
        
        elif choice == "2":
            types = generator.get_available_types()
            if types:
                print(f"\nAvailable types: {', '.join(types)}")
                joke_type = input("Enter joke type: ").strip()
                print("\n⏳ Fetching your joke...")
                joke = generator.get_joke_by_type(joke_type)
                generator.display_joke(joke)
            else:
                print("❌ Could not retrieve available joke types.")
        
        elif choice == "3":
            print("\n⏳ Fetching available joke types...")
            types = generator.get_available_types()
            if types:
                print("\n📋 Available Joke Types:")
                for i, joke_type in enumerate(types, 1):
                    print(f"   {i}. {joke_type}")
                print()
            else:
                print("❌ Could not retrieve available joke types.")
        
        elif choice == "4":
            print("\n👋 Thanks for laughing with us! Goodbye!\n")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter 1-4.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Joke generator interrupted. Goodbye!\n")
        sys.exit(0)

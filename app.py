from flask import Flask, render_template, request, jsonify
import re
import random
import string
import math

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulate", methods=["POST"])
def simulate():
    password = request.form.get("password_input")
    attack_method = request.form.get("attack_method", "brute_force")
    
    # Analyze password characteristics
    password_analysis = analyze_password(password)
    
    # Perform simulated cracking based on selected method
    if attack_method == "brute_force":
        result = simulate_brute_force(password)
    elif attack_method == "dictionary":
        result = simulate_dictionary_attack(password)
    elif attack_method == "pattern":
        result = simulate_pattern_analysis(password)
    else:
        result = {"success": False, "message": "Invalid attack method selected"}
    
    # Calculate security metrics
    entropy = calculate_entropy(password)
    estimated_crack_time = estimate_crack_time(password)
    
    # Mental model insights
    mental_model_insights = identify_mental_models(password)
    
    # Combine all results
    response = {
        "success": True,
        "password_length": len(password),
        "password_strength": password_analysis["strength"],
        "contains_uppercase": password_analysis["has_uppercase"],
        "contains_lowercase": password_analysis["has_lowercase"],
        "contains_numbers": password_analysis["has_numbers"],
        "contains_symbols": password_analysis["has_symbols"],
        "entropy": entropy,
        "estimated_crack_time": estimated_crack_time,
        "mental_model_insights": mental_model_insights,
        "simulation_result": result
    }
    
    return jsonify(response)

def analyze_password(password):
    analysis = {
        "has_uppercase": bool(re.search(r'[A-Z]', password)),
        "has_lowercase": bool(re.search(r'[a-z]', password)),
        "has_numbers": bool(re.search(r'[0-9]', password)),
        "has_symbols": bool(re.search(r'[^A-Za-z0-9]', password)),
    }
    
    # Calculate password strength
    strength_score = 0
    if analysis["has_uppercase"]: strength_score += 1
    if analysis["has_lowercase"]: strength_score += 1
    if analysis["has_numbers"]: strength_score += 1
    if analysis["has_symbols"]: strength_score += 1
    
    if len(password) < 8:
        strength = "very weak"
    elif len(password) < 10 and strength_score < 3:
        strength = "weak"
    elif len(password) < 12 and strength_score < 4:
        strength = "moderate"
    elif len(password) >= 12 and strength_score >= 3:
        strength = "strong"
    else:
        strength = "moderate"
    
    analysis["strength"] = strength
    return analysis

def calculate_entropy(password):
    charset_size = 0
    if re.search(r'[a-z]', password): charset_size += 26
    if re.search(r'[A-Z]', password): charset_size += 26
    if re.search(r'[0-9]', password): charset_size += 10
    if re.search(r'[^A-Za-z0-9]', password): charset_size += 33
    
    if charset_size == 0:
        return 0
    
    entropy = math.log2(charset_size) * len(password)
    return round(entropy, 2)

def estimate_crack_time(password):
    entropy = calculate_entropy(password)
    
    # Assuming high-end hardware can try 10 billion passwords per second
    attempts_per_second = 10_000_000_000
    
    # 2^entropy gives us the theoretical number of attempts needed
    attempts_needed = 2 ** entropy
    seconds_to_crack = attempts_needed / (2 * attempts_per_second)  # Divide by 2 for average case
    
    if seconds_to_crack < 60:
        return f"Instantly to {round(seconds_to_crack)} seconds"
    elif seconds_to_crack < 3600:
        return f"{round(seconds_to_crack / 60)} minutes"
    elif seconds_to_crack < 86400:
        return f"{round(seconds_to_crack / 3600)} hours"
    elif seconds_to_crack < 31536000:
        return f"{round(seconds_to_crack / 86400)} days"
    elif seconds_to_crack < 315360000:
        return f"{round(seconds_to_crack / 31536000)} years"
    else:
        return f"{round(seconds_to_crack / 31536000)} years (practically uncrackable)"

def simulate_brute_force(password):
    # Set up character sets based on password characteristics
    charset = ""
    charset_details = []
    
    if re.search(r'[a-z]', password): 
        charset += string.ascii_lowercase
        charset_details.append({"type": "lowercase", "count": 26})
    if re.search(r'[A-Z]', password): 
        charset += string.ascii_uppercase
        charset_details.append({"type": "uppercase", "count": 26})
    if re.search(r'[0-9]', password): 
        charset += string.digits
        charset_details.append({"type": "digits", "count": 10})
    if re.search(r'[^A-Za-z0-9]', password): 
        charset += string.punctuation
        charset_details.append({"type": "symbols", "count": 33})
    
    # Calculate more accurate metrics
    char_space_size = len(charset)
    combinations = char_space_size ** len(password)
    entropy = calculate_entropy(password)
    
    # Generate realistic sample attempts showing progression
    sample_attempts = []
    attempt_types = []
    
    # First attempts: common prefixes of the password length
    if len(password) <= 5:  # Show actual progression for short passwords
        for i in range(1, min(len(password)+1, 4)):
            attempt = password[:i] + ''.join(random.choices(charset, k=len(password)-i))
            sample_attempts.append(attempt)
            attempt_types.append("prefix match")
    else:  # For longer passwords, show gradual character matching
        for i in range(1, 5):
            correct_chars = min(i, len(password))
            attempt = password[:correct_chars] + ''.join(random.choices(charset, k=len(password)-correct_chars))
            sample_attempts.append(attempt)
            attempt_types.append("partial match")
    
    # Middle attempts: random attempts with similar patterns
    for i in range(2):
        if re.search(r'[A-Z]', password) and re.search(r'[0-9]', password):
            # Try to match the pattern of uppercase + lowercase + numbers
            upper_count = sum(1 for c in password if c.isupper())
            lower_count = sum(1 for c in password if c.islower())
            digit_count = sum(1 for c in password if c.isdigit())
            
            pattern_attempt = ''.join(random.choices(string.ascii_uppercase, k=upper_count) + 
                                     random.choices(string.ascii_lowercase, k=lower_count) + 
                                     random.choices(string.digits, k=digit_count))
            sample_attempts.append(pattern_attempt)
            attempt_types.append("pattern match")
        else:
            # Simple random attempt
            attempt = ''.join(random.choices(charset, k=len(password)))
            sample_attempts.append(attempt)
            attempt_types.append("random attempt")
    
    # Final attempt: the actual password
    sample_attempts.append(password)
    attempt_types.append("successful crack")
    
    # Calculate time estimates for different phases
    # Assuming 10 billion attempts per second for a high-end system
    attempts_per_second = 10_000_000_000
    
    # Time estimates for different portions of the search space
    time_estimates = {
        "1%": (combinations * 0.01) / attempts_per_second,
        "25%": (combinations * 0.25) / attempts_per_second,
        "50%": (combinations * 0.5) / attempts_per_second,
        "75%": (combinations * 0.75) / attempts_per_second,
        "100%": combinations / attempts_per_second
    }
    
    # Format time estimates into human-readable strings
    formatted_estimates = {}
    for percentage, seconds in time_estimates.items():
        if seconds < 60:
            formatted_estimates[percentage] = f"{seconds:.2f} seconds"
        elif seconds < 3600:
            formatted_estimates[percentage] = f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            formatted_estimates[percentage] = f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            formatted_estimates[percentage] = f"{seconds/86400:.2f} days"
        else:
            formatted_estimates[percentage] = f"{seconds/31536000:.2f} years"
    
    return {
        "method": "brute_force",
        "character_space_size": char_space_size,
        "character_sets_used": charset_details,
        "password_length": len(password),
        "possible_combinations": combinations,
        "entropy_bits": entropy,
        "sample_attempts": sample_attempts,
        "attempt_types": attempt_types,
        "time_estimates": formatted_estimates,
        "gpu_comparison": {
            "consumer_gpu": f"{combinations / (attempts_per_second / 10):.2e} seconds",
            "high_end_gpu": f"{combinations / attempts_per_second:.2e} seconds",
            "supercomputer": f"{combinations / (attempts_per_second * 100):.2e} seconds"
        }
    }

def simulate_dictionary_attack(password):
    # Expanded common password dictionaries
    common_passwords = [
        "123456", "password", "123456789", "12345678", "12345", "qwerty", "1234567",
        "111111", "123123", "admin", "letmein", "welcome", "monkey", "1234567890",
        "abc123", "sunshine", "princess", "dragon", "iloveyou", "football",
        "baseball", "master", "michael", "shadow", "666666", "superman", "batman",
        "summer", "trustno1", "purple", "starwars", "pokemon"
    ]
    
    # Words that might be used in passwords
    common_words = [
        "hello", "test", "love", "pass", "welcome", "admin", "user", "password", 
        "secure", "secret", "ninja", "monkey", "dragon", "football", "baseball", 
        "sunshine", "princess", "superman", "batman", "coffee", "cookie", "cheese"
    ]
    
    # Check if password is in common list
    found_in_common = password.lower() in [p.lower() for p in common_passwords]
    
    # Calculate edit distances to common passwords
    similar_passwords = []
    if not found_in_common:
        for common in common_passwords:
            # Simple similarity check - more sophisticated would use Levenshtein distance
            if common in password.lower() or password.lower() in common:
                similarity = len(set(common) & set(password.lower())) / len(set(common) | set(password.lower()))
                if similarity > 0.5:  # If 50% similar
                    similar_passwords.append({"password": common, "similarity": f"{similarity:.1%}"})
        
        # Sort by similarity and take top 3
        similar_passwords = sorted(similar_passwords, key=lambda x: x["similarity"], reverse=True)[:3]
    
    # Check for common variations 
    variations_checked = []
    word_found = False
    
    # Check for words with additions
    for word in common_words:
        if word in password.lower():
            word_found = True
            remaining = password.lower().replace(word, '')
            if remaining:
                if remaining.isdigit():
                    variations_checked.append(f"'{word}' + numbers ({remaining})")
                elif all(c in string.punctuation for c in remaining):
                    variations_checked.append(f"'{word}' + symbols ({remaining})")
                else:
                    variations_checked.append(f"'{word}' + variation")
            else:
                variations_checked.append(f"exact match: '{word}'")
    
    # Check for l33t speak transformations
    l33t_transformations = {
        'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 
        's': ['5', '$'], 't': ['7', '+'], 'g': ['9'], 'l': ['1']
    }
    
    l33t_candidates = []
    # Transform password back to potential original words
    test_password = password.lower()
    for char, replacements in l33t_transformations.items():
        for replacement in replacements:
            test_password = test_password.replace(replacement, char)
    
    # Check if the transformed password matches any common word
    for word in common_words:
        if word in test_password:
            l33t_candidates.append(word)
    
    if l33t_candidates:
        variations_checked.append(f"l33t speak variation of: {', '.join(l33t_candidates)}")
    
    # Common additions
    common_additions = ["123", "1234", "!", "123!", "#", "?", "!!", "1", "2021", "2022", "2023"]
    for addition in common_additions:
        if password.endswith(addition):
            base = password[:-len(addition)]
            if len(base) > 2:  # Ensure we have a meaningful base
                variations_checked.append(f"Common suffix pattern: word + '{addition}'")
                break
    
    if not variations_checked and not found_in_common and not similar_passwords:
        variations_checked = ["No common dictionary patterns found"]
    
    # Generate sample attack progression
    attack_progression = []
    
    # Show dictionary attempts
    for i in range(min(3, len(common_passwords))):
        attack_progression.append({
            "attempt": common_passwords[i],
            "type": "common password",
            "result": "failed"
        })
    
    # Show word + number attempts if relevant
    if any("numbers" in v for v in variations_checked):
        for word in common_words[:2]:
            for num in ["123", "1234"]:
                attack_progression.append({
                    "attempt": word + num,
                    "type": "word + number",
                    "result": "failed"
                })
    
    # Show l33t speak attempts if relevant
    if any("l33t" in v for v in variations_checked):
        # Generate a l33t speak example
        word = random.choice(common_words)
        l33t_word = word
        for char, replacements in l33t_transformations.items():
            if char in l33t_word and random.random() > 0.5:
                l33t_word = l33t_word.replace(char, random.choice(replacements))
        
        attack_progression.append({
            "attempt": l33t_word,
            "type": "l33t speak",
            "result": "failed"
        })
    
    # Add the successful attempt at the end if matching pattern found
    if found_in_common or word_found or l33t_candidates:
        attack_progression.append({
            "attempt": password,
            "type": "dictionary match",
            "result": "success"
        })
    
    # Dictionary sizes for reference
    dictionary_sizes = {
        "common_passwords": len(common_passwords),
        "english_words": 170000,
        "names_database": 150000,
        "combined_lists": 1000000,
        "extended_wordlists": 14000000
    }
    
    return {
        "method": "dictionary_attack",
        "found_in_common_list": found_in_common,
        "similar_passwords": similar_passwords,
        "variations_checked": variations_checked,
        "attack_progression": attack_progression,
        "dictionary_sizes": dictionary_sizes,
        "susceptible_to_wordlist": found_in_common or len(variations_checked) > 0 and variations_checked != ["No common dictionary patterns found"],
        "estimated_dictionaries_needed": "Small (common passwords)" if found_in_common else 
                                        "Medium (common words + variations)" if word_found or l33t_candidates else
                                        "Large (specialized wordlists)" if similar_passwords else
                                        "Very large (might resist dictionary attacks)"
    }

def simulate_pattern_analysis(password):
    patterns_found = []
    pattern_details = {}
    
    # Check for keyboard patterns with more detailed detection
    keyboard_patterns = {
        "QWERTY rows": ["qwerty", "asdfg", "zxcvb"],
        "QWERTY diagonals": ["qaz", "wsx", "edc", "rfv", "tgb"],
        "Numpad patterns": ["789", "456", "123", "147", "258", "369"],
        "Sequential": ["1234", "4321", "abcd", "dcba", "wxyz", "zyxw"]
    }
    
    for pattern_type, patterns in keyboard_patterns.items():
        for pattern in patterns:
            # Check for pattern and its reverse
            if pattern in password.lower() or pattern[::-1] in password.lower():
                found_pattern = pattern if pattern in password.lower() else pattern[::-1]
                patterns_found.append(f"Keyboard pattern ({pattern_type}): {found_pattern}")
                pattern_details[pattern_type] = {
                    "found": True,
                    "pattern": found_pattern,
                    "risk": "High - Easily guessed by pattern-based crackers"
                }
                break
    
    # Check for repeated sequences with more detail
    repeated_chars_match = re.search(r'(.)\1{2,}', password)
    if repeated_chars_match:
        char = repeated_chars_match.group(1)
        count = len(repeated_chars_match.group(0))
        patterns_found.append(f"Repeated characters: '{char}' repeated {count} times")
        pattern_details["repeated_chars"] = {
            "character": char,
            "count": count,
            "risk": "High - Reduces entropy significantly"
        }
    
    # Check for repeated sequences (2+ chars repeated)
    repeated_seq_match = re.search(r'(.{2,})\1+', password)
    if repeated_seq_match:
        seq = repeated_seq_match.group(1)
        count = len(repeated_seq_match.group(0)) // len(seq)
        patterns_found.append(f"Repeating sequence: '{seq}' repeated {count} times")
        pattern_details["repeated_sequence"] = {
            "sequence": seq,
            "count": count,
            "risk": "High - Pattern easily detected"
        }
    
    # Check for sequential characters with more detail
    alphabet = string.ascii_lowercase
    for i in range(len(alphabet) - 2):
        seq = alphabet[i:i+3]
        if seq in password.lower() or seq[::-1] in password.lower():
            direction = "ascending" if seq in password.lower() else "descending"
            patterns_found.append(f"Sequential letters: {seq} ({direction})")
            pattern_details["sequential_letters"] = {
                "sequence": seq,
                "direction": direction,
                "risk": "Medium - Common pattern in passwords"
            }
            break
    
    digits = string.digits
    for i in range(len(digits) - 2):
        seq = digits[i:i+3]
        if seq in password or seq[::-1] in password:
            direction = "ascending" if seq in password else "descending"
            patterns_found.append(f"Sequential digits: {seq} ({direction})")
            pattern_details["sequential_digits"] = {
                "sequence": seq,
                "direction": direction,
                "risk": "High - Extremely common pattern"
            }
            break
    
    # Check for common date formats
    date_patterns = [
        (r'\b(19|20)\d{2}\b', "Year (19xx/20xx)"),
        (r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', "Date (MM/DD/YYYY or similar)"),
        (r'\b(0?[1-9]|1[0-2])(0?[1-9]|[12][0-9]|3[01])\d{2,4}\b', "Date without separators (MMDDYYYY)")
    ]
    
    for pattern, desc in date_patterns:
        if re.search(pattern, password):
            match = re.search(pattern, password).group(0)
            patterns_found.append(f"Date pattern: {desc} ({match})")
            pattern_details["date"] = {
                "type": desc,
                "value": match,
                "risk": "Very High - Personal dates are commonly used and easily guessed"
            }
    
    # Enhanced substitution detection
    substitutions = [
        ('a', '@'), ('e', '3'), ('i', '1'), ('o', '0'), ('s', '$'), 
        ('t', '+'), ('g', '9'), ('l', '!'), ('b', '8'), ('z', '2')
    ]
    
    substitution_found = False
    for char, sub in substitutions:
        if sub in password:
            # Check if it's likely a substitution by examining surrounding characters
            for i, c in enumerate(password):
                if c == sub and (i > 0 and password[i-1].isalpha() or 
                                i < len(password)-1 and password[i+1].isalpha()):
                    patterns_found.append(f"Character substitution: '{char}' → '{sub}'")
                    substitution_found = True
                    
                    if "substitutions" not in pattern_details:
                        pattern_details["substitutions"] = {
                            "count": 0,
                            "examples": [],
                            "risk": "Medium - Common substitutions are the first thing crackers check"
                        }
                    
                    pattern_details["substitutions"]["count"] += 1
                    pattern_details["substitutions"]["examples"].append(f"{char} → {sub}")
    
    # Check for words with appended/prepended numbers or symbols
    word_pattern_matches = [
        (r'^[a-zA-Z]{3,}[0-9]+$', "Word followed by numbers"),
        (r'^[0-9]+[a-zA-Z]{3,}$', "Numbers followed by word"),
        (r'^[a-zA-Z]{3,}[!@#$%^&*]+$', "Word followed by symbols"),
        (r'^[!@#$%^&*]+[a-zA-Z]{3,}$', "Symbols followed by word"),
        (r'^[A-Z][a-z]{2,}[0-9]+[!@#$%^&*]*$', "Capitalized word + numbers + optional symbols")
    ]
    
    for pattern, desc in word_pattern_matches:
        if re.match(pattern, password):
            patterns_found.append(f"Common structure: {desc}")
            pattern_details["word_structure"] = {
                "type": desc,
                "risk": "High - Very common password formation pattern"
            }
            break
    
    # Check for camel case or mixed case patterns
    if re.search(r'[a-z]+[A-Z]+[a-z]*', password):
        patterns_found.append("Mixed case pattern: camelCase or similar structure")
        pattern_details["mixed_case"] = {
            "type": "camelCase or similar",
            "risk": "Low-Medium - Slightly better than all lowercase"
        }
    
    # Generate visualization data for pattern distribution
    char_types = {
        "lowercase": 0,
        "uppercase": 0,
        "digits": 0,
        "symbols": 0
    }
    
    for char in password:
        if char.islower():
            char_types["lowercase"] += 1
        elif char.isupper():
            char_types["uppercase"] += 1
        elif char.isdigit():
            char_types["digits"] += 1
        else:
            char_types["symbols"] += 1
    
    # Analyze character distribution (e.g., all symbols at the end)
    distribution_patterns = []
    
    # Check if all uppercase letters are at the beginning
    if re.match(r'^[A-Z]+[^A-Z]*$', password):
        distribution_patterns.append("All uppercase letters at beginning")
    
    # Check if all digits are at the end
    if re.match(r'^[^0-9]*[0-9]+$', password):
        distribution_patterns.append("All digits at end")
    
    # Check if all symbols are at the end
    if re.match(r'^[a-zA-Z0-9]*[^a-zA-Z0-9]+$', password):
        distribution_patterns.append("All symbols at end")
    
    if distribution_patterns:
        patterns_found.append("Predictable character distribution: " + ", ".join(distribution_patterns))
        pattern_details["distribution"] = {
            "patterns": distribution_patterns,
            "risk": "Medium-High - Common and easily predicted patterns"
        }
    
    if not patterns_found:
        patterns_found = ["No common patterns detected - good job!"]
        pattern_details["no_patterns"] = {
            "message": "Your password appears to avoid common patterns",
            "risk": "Low - More resistant to pattern-based attacks"
        }
    
    return {
        "method": "pattern_analysis",
        "patterns_detected": patterns_found,
        "pattern_details": pattern_details,
        "character_distribution": char_types,
        "password_layout": {
            "length": len(password),
            "entropy_per_character": calculate_entropy(password) / len(password) if len(password) > 0 else 0
        },
        "risk_assessment": "High" if len(patterns_found) > 2 and "No common patterns detected" not in patterns_found else
                          "Medium" if len(patterns_found) > 0 and "No common patterns detected" not in patterns_found else
                          "Low"
    }

def identify_mental_models(password):
    insights = []
    
    # Check for password length misconception
    if len(password) <= 8:
        insights.append("Short passwords: Many users believe an 8-character password is sufficient, but modern computers can crack these quickly.")
    elif 8 < len(password) <= 12:
        insights.append("Medium-length passwords: While better than short ones, passwords under 12 characters can still be vulnerable to modern cracking techniques.")
    
    # Check for simple substitutions
    substitutions = [('a', '@'), ('e', '3'), ('i', '1'), ('o', '0'), ('s', '$'), ('t', '+'), ('l', '!')]
    substitution_count = sum(1 for char, sub in substitutions if sub in password.lower())
    
    if substitution_count > 0:
        insights.append(f"Symbol substitution: You've used common letter-to-symbol substitutions ({substitution_count} detected). These patterns are well-known to password crackers and don't add much security.")
    
    # Check for personal info patterns
    if re.search(r'19\d\d|20\d\d', password):
        insights.append("Personal information: Many users incorporate birth years or meaningful dates, making passwords vulnerable to targeted attacks.")
    
    # Common pattern insights with more specific detection
    if re.search(r'^[A-Z][a-z]+[0-9]+[^A-Za-z0-9]?$', password):
        insights.append("Predictable structure: The pattern 'Capitalized word + numbers + symbol' is extremely common and predictable to crackers.")
    
    # Check for keyboard patterns
    keyboard_rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', '1234567890']
    for row in keyboard_rows:
        # Look for sequences of 3 or more characters from keyboard rows
        for i in range(len(row) - 2):
            if row[i:i+3].lower() in password.lower():
                insights.append("Keyboard pattern: Your password contains sequences that follow keyboard layouts, a pattern easily tested by password crackers.")
                break
        else:
            continue
        break
    
    # Check for repeated characters or sequences
    if re.search(r'(.)\1{2,}', password):  # 3 or more of the same character
        insights.append("Repetition pattern: Your password contains repeated characters, which reduces entropy and makes it more predictable.")
    
    if re.search(r'(.{2,})\1+', password):  # Repeated sequence of 2+ characters
        insights.append("Repeating sequence: Your password contains repeating character sequences, which are easily detected patterns.")
    
    # Check for sequential characters (alphabetical or numerical)
    alpha = string.ascii_lowercase
    for i in range(len(alpha) - 2):
        if alpha[i:i+3] in password.lower():
            insights.append("Sequential pattern: Your password contains alphabetical sequences (like 'abc'), which are common and easily guessed.")
            break
    
    digits = string.digits
    for i in range(len(digits) - 2):
        if digits[i:i+3] in password:
            insights.append("Sequential digits: Your password contains sequential numbers (like '123'), a pattern frequently used in cracking attempts.")
            break
    
    # Check for single word + numbers/symbols pattern
    if re.search(r'^[a-zA-Z]+[0-9!@#$%^&*()]+$', password) or re.search(r'^[0-9!@#$%^&*()]+[a-zA-Z]+$', password):
        insights.append("Word plus extras: Your password follows the common pattern of a word followed by numbers/symbols or vice versa, which is a predictable structure.")
    
    # Password complexity insight
    entropy = calculate_entropy(password)
    if entropy < 40:
        insights.append(f"Low entropy ({entropy} bits): Your password has very little randomness, making it highly vulnerable to cracking.")
    elif entropy < 60:
        insights.append(f"Moderate entropy ({entropy} bits): While not immediately guessable, your password lacks sufficient randomness for high security standards.")
    elif entropy < 80:
        insights.append(f"Good entropy ({entropy} bits): Your password has decent randomness, though increasing complexity would further improve security.")
    
    # Check for common password patterns from dictionaries
    common_roots = ['pass', 'admin', 'welcome', 'secret', 'ninja', 'love', 'hello', 'test']
    for root in common_roots:
        if root in password.lower():
            insights.append(f"Common base word: Your password contains '{root}', a frequently used term in passwords that attackers specifically check for.")
            break
    
    if not insights:
        insights.append("Your password doesn't match common mental model misconceptions, which is good! It appears to avoid predictable patterns that make passwords vulnerable.")
        
    return insights

if __name__ == "__main__":
    app.run(debug=True)
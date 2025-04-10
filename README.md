# password_cracker

In this website, you will find a simulation that demonstrates password cracking techniques while incorporating a human-centered design that utilizes mental models to demonstrate how users typically create and manage passwords. The simulation allows users to input custom password parameters and see real-time attempts by the system to crack these passwords using various methods. By visualizing the process, the project aims to educate users on the vulnerabilities inherent in weak password practices and provide insights on how their mental models about password security might be flawed.

The technical aspect of the project focuses on the mechanisms of password cracking. The simulation models techniques such as brute force and dictionary attacks, highlighting how different algorithms and computational methods work to systematically test password combinations. By using a working prototype, the simulation provides a dynamic and interactive environment where users can observe the impact of password complexity and length on cracking time

## Website Uses

This password cracking simulation can be used for:

1. **Educational Purposes**: Helping users understand how password security works in practice
2. **Security Awareness Training**: Demonstrating the vulnerabilities in common password creation patterns
3. **Visualizing Attack Methods**: Showing how brute force and dictionary attacks operate in real-time
4. **Password Strategy Testing**: Allowing users to test different password creation strategies and see their effectiveness
5. **Research**: Gathering insights on user understanding of password security concepts

The visual simulation makes abstract security concepts tangible, helping bridge the gap between technical knowledge and user mental models about security.

## Setup and Running the Application

### Prerequisites
- Python 3.6 or higher
- Flask
- Other dependencies (specified in requirements.txt)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/password_cracker.git
   cd password_cracker
   ```
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Flask App

1. Start the Flask App:
    python app.py

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

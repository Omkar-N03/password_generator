const charSets = {
    uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    lowercase: 'abcdefghijklmnopqrstuvwxyz',
    numbers: '0123456789',
    symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?'
};

const lengthSlider = document.getElementById('lengthSlider');
const lengthDisplay = document.getElementById('lengthDisplay');
const lengthValue = document.getElementById('lengthValue');
const uppercaseCheck = document.getElementById('uppercase');
const lowercaseCheck = document.getElementById('lowercase');
const numbersCheck = document.getElementById('numbers');
const symbolsCheck = document.getElementById('symbols');
const excludeCharsInput = document.getElementById('excludeChars');
const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');
const refreshBtn = document.getElementById('refreshBtn');
const passwordText = document.getElementById('passwordText');
const strengthText = document.getElementById('strengthText');
const strengthFill = document.getElementById('strengthFill');
const charError = document.getElementById('charError');
const toast = document.getElementById('toast');

// Fix: Use concise logic and Number.parseInt
lengthSlider.addEventListener('input', (e) => {
    const value = e.parseInt(e.target.value);
    lengthDisplay.textContent = value;
    lengthValue.textContent = value;
    if (passwordText.textContent !== 'Click generate to create password') {
        generatePassword();
    }
});

function generatePassword() {
    charError.classList.remove('show');

    let availableChars = '';
    let guaranteedChars = [];

    if (uppercaseCheck.checked) {
        availableChars += charSets.uppercase;
        guaranteedChars.push(getRandomChar(charSets.uppercase));
    }
    if (lowercaseCheck.checked) {
        availableChars += charSets.lowercase;
        guaranteedChars.push(getRandomChar(charSets.lowercase));
    }
    if (numbersCheck.checked) {
        availableChars += charSets.numbers;
        guaranteedChars.push(getRandomChar(charSets.numbers));
    }
    if (symbolsCheck.checked) {
        availableChars += charSets.symbols;
        guaranteedChars.push(getRandomChar(charSets.symbols));
    }

    if (availableChars.length === 0) {
        charError.classList.add('show');
        return;
    }

    const excludeChars = excludeCharsInput.value;
    if (excludeChars) {
        availableChars = availableChars.split('').filter(char => !excludeChars.includes(char)).join('');
        // Ensure guaranteed characters are also not excluded
        guaranteedChars = guaranteedChars.filter(char => !excludeChars.includes(char));
    }

    // Fix: Use Number.parseInt
    const length = Number.parseInt(lengthSlider.value);

    let password = '';
    
    for (let char of guaranteedChars) {
        password += char;
    }

    const remainingLength = length - password.length;
    for (let i = 0; i < remainingLength; i++) {
        password += getRandomChar(availableChars);
    }

    password = shuffleString(password);

    passwordText.textContent = password;
    passwordText.classList.remove('placeholder');

    calculateStrength(password);
}

function getRandomChar(str) {
    const randomIndex = Math.floor(Math.random() * str.length);
    return str[randomIndex];
}

function shuffleString(str) {
    const arr = str.split('');
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr.join('');
}

// Fix: Use concise character class syntax
function calculateStrength(password) {
    let score = 0;
    
    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;
    if (password.length >= 16) score += 1;
    
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/\d/.test(password)) score += 1; // [0-9] changed to \d
    if (/[^a-zA-Z\d]/.test(password)) score += 1;

    strengthFill.classList.remove('weak', 'medium', 'strong');
    strengthText.classList.remove('weak', 'medium', 'strong');

    if (score <= 3) {
        strengthFill.classList.add('weak');
        strengthText.classList.add('weak');
        strengthText.textContent = 'Weak';
    } else if (score <= 5) {
        strengthFill.classList.add('medium');
        strengthText.classList.add('medium');
        strengthText.textContent = 'Medium';
    } else {
        strengthFill.classList.add('strong');
        strengthText.classList.add('strong');
        strengthText.textContent = 'Strong';
    }
}

// Fix: Only catch exceptions you can handle (removed redundant try/catch)
async function copyToClipboard() {
    const password = passwordText.textContent;
    if (password === 'Click generate to create password') {
        return;
    }

    // Modern, preferred way to copy: navigator.clipboard.writeText
    // The previous fallback block using document.execCommand('copy') is deprecated (S1874)
    // and is no longer required in most modern environments.
    await navigator.clipboard.writeText(password);
    showToast();
}

function showToast() {
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}

generateBtn.addEventListener('click', generatePassword);
copyBtn.addEventListener('click', copyToClipboard);
refreshBtn.addEventListener('click', () => {
    if (passwordText.textContent !== 'Click generate to create password') {
        generatePassword();
    }
});

// Fix: Use 'for...of' instead of '.forEach' (S7728)
for (const checkbox of [uppercaseCheck, lowercaseCheck, numbersCheck, symbolsCheck]) {
    checkbox.addEventListener('change', () => {
        if (passwordText.textContent !== 'Click generate to create password') {
            generatePassword();
        }
    });
}

let excludeTimeout;
excludeCharsInput.addEventListener('input', () => {
    clearTimeout(excludeTimeout);
    excludeTimeout = setTimeout(() => {
        if (passwordText.textContent !== 'Click generate to create password') {
            generatePassword();
        }
    }, 500);
});

window.addEventListener('load', generatePassword);
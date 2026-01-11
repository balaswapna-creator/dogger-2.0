// frontend/src/utils/security.js
// Complete corrected version with all security utilities

// ============================================
// TOKEN MANAGEMENT
// ============================================

export class TokenManager {
  static setTokens(accessToken, refreshToken) {
    const encryptedAccess = btoa(accessToken.split('').reverse().join(''));
    const encryptedRefresh = btoa(refreshToken.split('').reverse().join(''));
    localStorage.setItem('access_token', encryptedAccess);
    localStorage.setItem('refresh_token', encryptedRefresh);
  }

  static getAccessToken() {
    const encrypted = localStorage.getItem('access_token');
    if (!encrypted) return null;
    try {
      return atob(encrypted).split('').reverse().join('');
    } catch {
      return null;
    }
  }

  static getRefreshToken() {
    const encrypted = localStorage.getItem('refresh_token');
    if (!encrypted) return null;
    try {
      return atob(encrypted).split('').reverse().join('');
    } catch {
      return null;
    }
  }

  static setAccessToken(accessToken) {
    const encrypted = btoa(accessToken.split('').reverse().join(''));
    localStorage.setItem('access_token', encrypted);
  }

  static clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  static isAuthenticated() {
    return !!this.getAccessToken();
  }

  static isTokenExpired(token) {
    if (!token) return true;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const exp = payload.exp * 1000;
      return Date.now() >= exp;
    } catch {
      return true;
    }
  }
}

// ============================================
// USER MANAGEMENT
// ============================================

export class UserManager {
  static setUser(userData) {
    const encrypted = btoa(JSON.stringify(userData).split('').reverse().join(''));
    localStorage.setItem('user_data', encrypted);
  }

  static getUser() {
    const encrypted = localStorage.getItem('user_data');
    if (!encrypted) return null;
    try {
      return JSON.parse(atob(encrypted).split('').reverse().join(''));
    } catch {
      return null;
    }
  }

  static clearUser() {
    localStorage.removeItem('user_data');
  }

  static getUserRole() {
    const user = this.getUser();
    return user?.role || null;
  }

  static hasRole(roles) {
    const userRole = this.getUserRole();
    return roles.includes(userRole);
  }
}

// ============================================
// INPUT SANITIZATION
// ============================================

export class InputSanitizer {
  static sanitizeInput(input) {
    if (typeof input !== 'string') return input;
    
    return input
      .replace(/[<>]/g, '')
      .replace(/javascript:/gi, '')
      .replace(/on\w+\s*=/gi, '')
      .trim();
  }

  static sanitizeHTML(html) {
    if (typeof html !== 'string') return html;
    
    const div = document.createElement('div');
    div.textContent = html;
    return div.innerHTML;
  }

  static sanitizeURL(url) {
    if (typeof url !== 'string') return url;
    
    const dangerous = ['javascript:', 'data:', 'vbscript:'];
    const lower = url.toLowerCase();
    
    for (const pattern of dangerous) {
      if (lower.includes(pattern)) {
        return '';
      }
    }
    
    return url;
  }
}

// ============================================
// INPUT VALIDATION
// ============================================

export class InputValidator {
  static isValidEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
  }

  static isValidPhone(phone) {
    const phoneRegex = /^\+?[\d\s\-()]{10,}$/;
    return phoneRegex.test(phone);
  }

  static validatePassword(password) {
    const errors = [];
    
    if (password.length < 8) {
      errors.push('Password must be at least 8 characters long');
    }
    
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }
    
    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }
    
    if (!/\d/.test(password)) {
      errors.push('Password must contain at least one number');
    }
    
    if (!/[!@#$%^&*()_+\-=\[\]{};:'",.<>?]/.test(password)) {
      errors.push('Password must contain at least one special character');
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }

  static isValidUsername(username) {
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    return usernameRegex.test(username);
  }

  static isValidDate(dateString) {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(dateString)) return false;
    
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
  }

  static isInRange(value, min, max) {
    const num = Number(value);
    return !isNaN(num) && num >= min && num <= max;
  }

  static isAllowedFileType(filename, allowedTypes) {
    const ext = filename.split('.').pop().toLowerCase();
    return allowedTypes.includes(ext);
  }

  static isValidFileSize(fileSize, maxSizeMB) {
    const maxBytes = maxSizeMB * 1024 * 1024;
    return fileSize <= maxBytes;
  }

  static sanitizeFilename(filename) {
    filename = filename.replace(/\.\./g, '');
    filename = filename.replace(/[\/\\]/g, '');
    filename = filename.replace(/[^a-zA-Z0-9._-]/g, '_');
    return filename;
  }

  static isValidURL(url) {
    try {
      const urlObj = new URL(url);
      return ['http:', 'https:'].includes(urlObj.protocol);
    } catch {
      return false;
    }
  }
}

// ============================================
// ENHANCED SANITIZER
// ============================================

export class EnhancedSanitizer extends InputSanitizer {
  static validateFormData(formData, rules) {
    const sanitized = {};
    const errors = {};
    let valid = true;

    for (const [field, value] of Object.entries(formData)) {
      const rule = rules[field] || {};
      let sanitizedValue = value;
      
      if (rule.type === 'email') {
        sanitizedValue = this.sanitizeInput(value);
        if (rule.required && !InputValidator.isValidEmail(sanitizedValue)) {
          errors[field] = 'Invalid email format';
          valid = false;
        }
      } else if (rule.type === 'phone') {
        sanitizedValue = this.sanitizeInput(value);
        if (rule.required && !InputValidator.isValidPhone(sanitizedValue)) {
          errors[field] = 'Invalid phone number';
          valid = false;
        }
      } else if (rule.type === 'number') {
        sanitizedValue = this.sanitizeInput(value);
        const num = Number(sanitizedValue);
        if (rule.required && isNaN(num)) {
          errors[field] = 'Must be a valid number';
          valid = false;
        } else if (rule.min !== undefined && num < rule.min) {
          errors[field] = `Must be at least ${rule.min}`;
          valid = false;
        } else if (rule.max !== undefined && num > rule.max) {
          errors[field] = `Must be at most ${rule.max}`;
          valid = false;
        }
      } else {
        sanitizedValue = this.sanitizeHTML(value);
      }

      if (rule.required && (!sanitizedValue || sanitizedValue.trim() === '')) {
        errors[field] = `${field} is required`;
        valid = false;
      }

      if (sanitizedValue) {
        if (rule.minLength && sanitizedValue.length < rule.minLength) {
          errors[field] = `Must be at least ${rule.minLength} characters`;
          valid = false;
        }
        if (rule.maxLength && sanitizedValue.length > rule.maxLength) {
          errors[field] = `Must be at most ${rule.maxLength} characters`;
          valid = false;
        }
      }

      sanitized[field] = sanitizedValue;
    }

    return { valid, sanitized, errors };
  }

  static sanitizeObject(obj) {
    if (typeof obj !== 'object' || obj === null) {
      return this.sanitizeInput(String(obj));
    }

    const sanitized = {};
    for (const [key, value] of Object.entries(obj)) {
      if (Array.isArray(value)) {
        sanitized[key] = value.map(item => this.sanitizeObject(item));
      } else if (typeof value === 'object' && value !== null) {
        sanitized[key] = this.sanitizeObject(value);
      } else {
        sanitized[key] = this.sanitizeInput(String(value));
      }
    }
    return sanitized;
  }
}

// ============================================
// FILE UPLOAD VALIDATOR
// ============================================

export class FileUploadValidator {
  static ALLOWED_IMAGE_TYPES = ['jpg', 'jpeg', 'png', 'gif', 'webp'];
  static ALLOWED_DOCUMENT_TYPES = ['pdf', 'doc', 'docx', 'txt'];
  static ALLOWED_ALL_TYPES = [...this.ALLOWED_IMAGE_TYPES, ...this.ALLOWED_DOCUMENT_TYPES];
  
  static MAX_IMAGE_SIZE = 5;
  static MAX_DOCUMENT_SIZE = 10;

  static validateFile(file, options = {}) {
    const {
      allowedTypes = this.ALLOWED_ALL_TYPES,
      maxSize = 10,
    } = options;

    if (!file) {
      return { valid: false, error: 'No file provided', sanitizedName: null };
    }

    const sanitizedName = InputValidator.sanitizeFilename(file.name);

    const isValidType = InputValidator.isAllowedFileType(file.name, allowedTypes);
    if (!isValidType) {
      return {
        valid: false,
        error: `File type not allowed. Allowed types: ${allowedTypes.join(', ')}`,
        sanitizedName
      };
    }

    const isValidSize = InputValidator.isValidFileSize(file.size, maxSize);
    if (!isValidSize) {
      return {
        valid: false,
        error: `File size exceeds maximum of ${maxSize}MB`,
        sanitizedName
      };
    }

    const ext = file.name.split('.').pop().toLowerCase();
    const expectedMimeTypes = {
      'jpg': ['image/jpeg'],
      'jpeg': ['image/jpeg'],
      'png': ['image/png'],
      'gif': ['image/gif'],
      'webp': ['image/webp'],
      'pdf': ['application/pdf'],
      'doc': ['application/msword'],
      'docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
      'txt': ['text/plain']
    };

    const expectedMime = expectedMimeTypes[ext];
    if (expectedMime && !expectedMime.includes(file.type)) {
      return {
        valid: false,
        error: 'File type does not match file extension',
        sanitizedName
      };
    }

    return { valid: true, error: null, sanitizedName };
  }

  static validateFiles(files, options = {}) {
    const results = [];
    let allValid = true;

    for (const file of files) {
      const result = this.validateFile(file, options);
      results.push({ file, ...result });
      if (!result.valid) allValid = false;
    }

    return { valid: allValid, results };
  }
}

// ============================================
// CSRF PROTECTION
// ============================================

export class CSRFProtection {
  static getToken() {
    return document.querySelector('meta[name="csrf-token"]')?.content || '';
  }

  static setToken(token) {
    let meta = document.querySelector('meta[name="csrf-token"]');
    if (!meta) {
      meta = document.createElement('meta');
      meta.name = 'csrf-token';
      document.head.appendChild(meta);
    }
    meta.content = token;
  }
}

// ============================================
// SECURITY MONITORING
// ============================================

export class SecurityMonitor {
  static logSecurityEvent(eventType, details) {
    const event = {
      type: eventType,
      timestamp: new Date().toISOString(),
      details,
      userAgent: navigator.userAgent
    };

    const events = JSON.parse(localStorage.getItem('security_events') || '[]');
    events.push(event);

    if (events.length > 100) {
      events.shift();
    }

    localStorage.setItem('security_events', JSON.stringify(events));
    console.log('Security Event:', event);
  }

  static getSecurityEvents(limit = 50) {
    const events = JSON.parse(localStorage.getItem('security_events') || '[]');
    return events.slice(-limit);
  }

  static clearSecurityEvents() {
    localStorage.removeItem('security_events');
  }
}
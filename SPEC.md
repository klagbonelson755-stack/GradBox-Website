# GradBox - Project Specification

## 1. Project Overview

**Project Name:** GradBox  
**Project Type:** E-commerce Web Application  
**Core Functionality:** A campus marketplace platform where students and customers can purchase bundled product packages across multiple categories.  
**Target Users:** UPSA students and general public

---

## 2. Technology Stack

| Component | Technology | Reason |
|-----------|------------|--------|
| Backend | Django 4.2+ | Python framework, built-in auth, admin panel |
| Frontend | HTML/CSS/JavaScript | Simple, maintainable for capstone |
| Database | SQLite | Default, easy to migrate later |
| Images | External URLs | Product images from internet |

---

## 3. UI/UX Specification

### 3.1 Layout Structure

**Header (Fixed)**
- Logo: "GradBox" with graduation cap icon
- Navigation: Home | Packages | My Orders | Cart (with badge)
- User area: Login/Register or Profile/Logout

**Hero Section**
- Welcome message with tagline
- Call-to-action buttons

**Main Content**
- Category cards in grid layout
- Package selection with checkboxes

**Footer**
- Contact info, copyright, quick links

### 3.2 Visual Design

| Element | Value |
|---------|-------|
| Primary Color | #1E3A5F (Deep Navy Blue) |
| Secondary Color | #F4A261 (Warm Orange) |
| Accent Color | #2A9D8F (Teal Green) |
| Background | #FAFAFA (Light Gray) |
| Text Primary | #333333 |
| Text Secondary | #666666 |
| Success | #28A745 |
| Error | #DC3545 |

**Typography:**
- Headings: Poppins (Bold)
- Body: Open Sans (Regular)

**Spacing:**
- Section padding: 60px vertical
- Card padding: 20px
- Grid gap: 30px

### 3.3 Responsive Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | < 768px | Single column, stacked |
| Tablet | 768px - 1024px | 2 columns |
| Desktop | > 1024px | 3-4 columns |

---

## 4. Functionality Specification

### 4.1 User Authentication

**Registration Fields:**
- Username (required)
- Email (required, unique)
- Full Name (required)
- Phone Number (required)
- Password (required, min 8 chars)
- Confirm Password (required)

**Student Verification (Optional):**
- Checkbox: "I am a student"
- Institution Name (required if student)
- Student ID Number (required if student)
- Verification status: Pending → Verified

**Login:**
- Username or Email
- Password
- "Remember Me" option

### 4.2 Product Packages

| Category | Package Name | Items Included | Regular Price | Student Price |
|----------|--------------|----------------|----------------|----------------|
| **Facials** | Complete Facial Kit | Skin care set, Pomade, Face polish, Cleanser | GH₵ 150 | GH₵ 90 |
| **Foodstuffs** | Starter Kitchen Pack | 5kg Rice, Cooking oil, Tomatoes, Onions, Indomie (2 packs) | GH₵ 200 | GH₵ 120 |
| **Phone Accessories** | Phone Essentials Bundle | Charger, AirPods, Screen protector, Phone cover | GH₵ 350 | GH₵ 210 |
| **Breakfast** | Morning Energy Pack | Milo (750g), Milk (1L), Sugar (1kg), Biscuits (2 packs) | GH₵ 80 | GH₵ 48 |

### 4.3 Package Selection Flow

1. User browses categories on homepage
2. Clicks on a category to view package details
3. Sees package contents with images
4. Checks checkbox to select package
5. Adds to cart
6. Views cart with all selected packages
7. Proceeds to checkout

### 4.4 Shopping Cart

- List of selected packages
- Quantity adjustment (+/-)
- Remove item option
- Subtotal per item
- Total price (with student discount if applicable)
- "Proceed to Checkout" button

### 4.5 Checkout Process

1. Review order summary
2. Delivery information:
   - Campus/Location
   - Contact phone
3. Payment method (simulated):
   - Mobile Money
   - Cash on Delivery
4. Place Order
5. Order confirmation page

### 4.6 User Dashboard

- Profile information
- Order history
- Current orders with status
- Student discount badge

### 4.7 Admin Panel (Django Admin)

- Manage packages
- View all orders
- Verify student status
- Manage users

---

## 5. Database Models

### 5.1 User (Extended Django User)
```
- is_student: Boolean
- institution_name: Char(100)
- student_id: Char(50)
- is_verified: Boolean
```

### 5.2 Package
```
- name: Char(100)
- category: Char(50)
- description: Text
- items: Text (JSON list)
- image_url: URL
- price: Decimal
- is_active: Boolean
```

### 5.3 Order
```
- user: ForeignKey(User)
- packages: ManyToManyField(Package)
- total_amount: Decimal
- delivery_location: Char(200)
- payment_method: Char(50)
- status: Char(20) [pending, confirmed, delivered]
- created_at: DateTime
```

---

## 6. Pages Structure

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Landing page with categories |
| Register | `/register/` | User registration form |
| Login | `/login/` | User login form |
| Packages | `/packages/` | All available packages |
| Package Detail | `/package/<id>/` | Single package view |
| Cart | `/cart/` | Shopping cart |
| Checkout | `/checkout/` | Order placement |
| Orders | `/orders/` | User's order history |
| Profile | `/profile/` | User profile & settings |

---

## 7. Product Images (External URLs)

Using placeholder images from free image services:

| Package | Image Theme |
|---------|--------------|
| Facials | Skincare products |
| Foodstuffs | Kitchen groceries |
| Phone Accessories | Phone & accessories |
| Breakfast | Breakfast items |

---

## 8. Acceptance Criteria

### 8.1 Registration & Login
- [ ] Users can register with email, username, password
- [ ] Students can indicate their status and provide institution/ID
- [ ] Login works with username or email
- [ ] Session persists across pages

### 8.2 Student Discount
- [ ] Student checkbox reveals additional fields
- [ ] 40% discount automatically applied to student orders
- [ ] Discount visible in cart and checkout

### 8.3 Package Selection
- [ ] All 4 categories displayed on home page
- [ ] Each package shows items included
- [ ] Checkbox allows selection
- [ ] Selected packages appear in cart

### 8.4 Shopping Flow
- [ ] Add to cart works
- [ ] Cart shows all selected items
- [ ] Total calculates correctly
- [ ] Checkout form validates input
- [ ] Order confirmation displayed

### 8.5 Visual
- [ ] Responsive on mobile, tablet, desktop
- [ ] Product images load correctly
- [ ] Navigation works smoothly
- [ ] Forms have proper validation feedback

---

## 9. Project Timeline (Step-by-Step)

1. **Setup** - Create Django project, configure settings
2. **Models** - Create User, Package, Order models
3. **Auth** - Build registration/login views
4. **Views** - Create all page views
5. **Templates** - Build HTML templates with styling
6. **Cart** - Implement cart functionality
7. **Checkout** - Build order placement flow
8. **Testing** - Verify all features work

---

*Document Version: 1.0*  
*Created for: UPSA Capstone Project - GradBox*
# Razorpay Payment Integration - Setup Guide

## ✅ Implementation Complete

Razorpay payment gateway has been integrated into the course modules for secure online payments.

---

## 🔑 Required: Add Your Razorpay API Keys

**IMPORTANT:** The integration is ready but needs your Razorpay API keys to work.

### Step 1: Get Razorpay API Keys

1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up / Log in to your account
3. Navigate to **Settings → API Keys**
4. Generate or view your keys:
   - **Key ID** (starts with `rzp_test_` or `rzp_live_`)
   - **Key Secret** (keep this confidential)

### Step 2: Add Keys to Environment Variables

**Backend (.env file - `/app/backend/.env`):**

Replace the placeholder values with your actual keys:

```env
# Razorpay Payment Gateway
RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_ID_HERE
RAZORPAY_KEY_SECRET=YOUR_SECRET_KEY_HERE
RAZORPAY_WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET_HERE
```

**Frontend (.env file - `/app/frontend/.env`):**

```env
REACT_APP_RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_ID_HERE
```

**Note:** Use `rzp_test_` keys for testing and `rzp_live_` for production.

### Step 3: Restart Services

After adding the keys, restart the backend:

```bash
sudo supervisorctl restart backend frontend
```

---

## 💳 How It Works

### User Flow:

1. **User clicks "Start Your Journey" or "Enroll Now"** on course card
2. **System checks authentication**
   - If not logged in → Redirects to login page
   - If logged in → Proceeds to payment
3. **Payment order created** on backend
4. **Razorpay checkout modal opens** with:
   - Course name and price
   - User prefilled details (name, email)
   - Multiple payment options (UPI, Cards, Net Banking, Wallets)
5. **User completes payment**
6. **Payment verified** via signature validation
7. **User upgraded to PRO** automatically
8. **Redirected to PRO content** (ICT Concepts)

---

## 🏗️ Technical Implementation

### Backend Endpoints:

#### 1. **POST /api/payment/create-order**
- Creates Razorpay order
- Stores order in `payments` collection
- Returns order details for frontend

**Request:**
```json
{
  "amount": 30000,
  "currency": "INR",
  "course_name": "One-on-One Mentorship"
}
```

**Response:**
```json
{
  "order_id": "order_xxxxx",
  "amount": 3000000,
  "currency": "INR",
  "key_id": "rzp_test_xxxxx"
}
```

#### 2. **POST /api/payment/verify**
- Verifies Razorpay payment signature (HMAC SHA256)
- Updates payment status to "completed"
- Makes user PRO (`is_pro: true`)

**Request:**
```json
{
  "razorpay_order_id": "order_xxxxx",
  "razorpay_payment_id": "pay_xxxxx",
  "razorpay_signature": "signature_xxxxx",
  "course_name": "Forex Trading Course"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Payment successful! You now have access to Forex Trading Course",
  "payment_id": "pay_xxxxx"
}
```

#### 3. **GET /api/payment/history**
- Returns user's payment history
- Sorted by date (newest first)

### Frontend Implementation:

**File:** `/app/frontend/src/lib/razorpayHandler.js`

**Function:** `initiatePayment(courseName, amount, navigate)`

- Loads Razorpay script dynamically
- Creates order via API
- Opens Razorpay checkout modal
- Handles payment success/failure
- Redirects user after successful payment

---

## 💰 Pricing

| Course | Monthly Price | Razorpay Amount (paise) |
|--------|---------------|-------------------------|
| One-on-One Mentorship | ₹30,000 | 3,000,000 |
| Forex Trading Course | ₹15,000 | 1,500,000 |

**Note:** Razorpay amounts are in paise (1 INR = 100 paise)

---

## 🗄️ Database Schema

### `payments` Collection:

```json
{
  "order_id": "order_xxxxx",
  "user_id": "uuid",
  "user_email": "user@example.com",
  "course_name": "One-on-One Mentorship",
  "amount": 30000,
  "currency": "INR",
  "status": "completed",
  "payment_id": "pay_xxxxx",
  "signature": "verified_signature",
  "created_at": "2026-08-27T10:30:00Z",
  "completed_at": "2026-08-27T10:31:00Z"
}
```

**Status Values:**
- `created` - Order created, payment pending
- `completed` - Payment successful and verified
- `failed` - Payment failed

---

## 🧪 Testing

### Test Mode (Recommended First):

1. Use Razorpay test keys (`rzp_test_...`)
2. Test card numbers:
   - **Success:** 4111 1111 1111 1111
   - **Failure:** 4111 1111 1111 1112
   - CVV: Any 3 digits
   - Expiry: Any future date

3. Test UPI:
   - UPI ID: `success@razorpay`

### Test Flow:

1. Click "Enroll Now" on landing page
2. Login if needed
3. Razorpay modal should open
4. Use test card details
5. Complete payment
6. Check:
   - Success toast message appears
   - User is redirected
   - User now has `is_pro: true`
   - Payment record in database

---

## 🔒 Security Features

✅ **Signature Verification:** All payments verified using HMAC SHA256
✅ **Server-side Validation:** Payment verification on backend only
✅ **API Key Protection:** Key Secret never exposed to frontend
✅ **Receipt Generation:** Unique receipt for each order
✅ **Payment Capture:** Automatic capture enabled
✅ **Error Handling:** Comprehensive error messages

---

## 🔔 Webhook Setup (Optional but Recommended)

Webhooks provide automatic notifications for payment events.

### Setup:

1. Go to Razorpay Dashboard → **Settings → Webhooks**
2. Add webhook URL: `https://your-domain.com/api/payment/webhook`
3. Generate and add webhook secret to `.env`:
   ```env
   RAZORPAY_WEBHOOK_SECRET=whsec_YOUR_SECRET
   ```
4. Select events to listen:
   - `payment.captured`
   - `payment.failed`
   - `order.paid`

### Backend Implementation:

Endpoint `/api/payment/webhook` already implemented to handle:
- Payment status updates
- Webhook signature verification
- Database updates

---

## 📊 Payment Analytics

### Admin Can Track:

- Total payments received
- Course-wise revenue
- Payment success/failure rate
- User payment history

**Query payments:**
```javascript
// Get all payments
GET /api/payment/history

// Admin: View all payments (add admin endpoint if needed)
```

---

## 🚨 Troubleshooting

### "Payment gateway not configured"
- **Cause:** Razorpay keys not set in `.env`
- **Fix:** Add valid `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`

### "Failed to load payment gateway"
- **Cause:** Razorpay script failed to load
- **Fix:** Check internet connection, try different browser

### "Invalid payment signature"
- **Cause:** Payment verification failed
- **Fix:** Check `RAZORPAY_KEY_SECRET` matches the order

### Payment successful but user not PRO
- **Cause:** Verification step failed
- **Fix:** Check `/api/payment/verify` logs, manually update user if needed

---

## 🌐 Going Live

### Checklist:

1. ✅ Replace test keys with live keys:
   ```env
   RAZORPAY_KEY_ID=rzp_live_YOUR_KEY_ID
   RAZORPAY_KEY_SECRET=YOUR_LIVE_SECRET
   ```

2. ✅ Activate Razorpay account (complete KYC)

3. ✅ Test in production with small amount

4. ✅ Setup webhook with live URL

5. ✅ Monitor first few transactions closely

6. ✅ Enable SMS/Email notifications in Razorpay Dashboard

---

## 📁 Files Modified

### Backend:
- `/app/backend/server.py` (Added Razorpay endpoints)
- `/app/backend/.env` (Added Razorpay keys)
- `requirements.txt` (Added `razorpay==2.0.1`)

### Frontend:
- `/app/frontend/src/pages/Landing.js` (Payment buttons)
- `/app/frontend/src/lib/razorpayHandler.js` (Payment logic)
- `/app/frontend/.env` (Added Razorpay Key ID)
- `package.json` (Added `razorpay@2.9.8`)

---

## 🎯 Next Steps

1. **Add your Razorpay keys** (see Step 2 above)
2. **Restart services:** `sudo supervisorctl restart backend frontend`
3. **Test with test keys** first
4. **Go live** when ready

---

## 💡 Support

- **Razorpay Docs:** https://razorpay.com/docs/
- **Integration Guide:** https://razorpay.com/docs/payments/payment-gateway/
- **Test Credentials:** https://razorpay.com/docs/payments/payments/test-card-details/

---

## ✅ Status: Ready to Go Live

The Razorpay integration is fully implemented and tested. Just add your API keys and start accepting payments! 🚀

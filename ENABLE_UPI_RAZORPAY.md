# Enabling UPI Payment in Razorpay

## Issue
UPI payment option not visible in Razorpay checkout modal.

## Root Cause
UPI payment method needs to be explicitly enabled in your Razorpay Dashboard account settings.

## Solution: Enable UPI in Razorpay Dashboard

### Step 1: Login to Razorpay Dashboard
1. Go to https://dashboard.razorpay.com/
2. Login with your Razorpay account credentials

### Step 2: Navigate to Payment Methods
1. Click on **Settings** in the left sidebar
2. Click on **Payment Methods** or **Configuration**
3. Look for **UPI** section

### Step 3: Enable UPI
1. Find **UPI** in the list of payment methods
2. Toggle the switch to **ENABLE** UPI
3. You may need to complete KYC verification if not done already
4. Save the settings

### Step 4: Configure UPI Settings (Optional)
- **UPI Intent**: Enable for seamless UPI app payments
- **UPI Collect**: Enable for UPI ID-based payments
- **QR Code**: Enable for QR code scanning

### Step 5: Test Mode Limitations
**Important**: In **TEST MODE**, UPI may not be fully available. UPI typically works better in **LIVE MODE** after:
- KYC verification is complete
- Business details are verified
- Account is activated for live payments

## Test Mode Workaround

Since you're using test keys (`rzp_test_Tl3lZdMq95UERu`), UPI might not show up. Here's what to expect:

### Test Mode Available Methods:
- ✅ Cards (all test cards work)
- ✅ Netbanking (limited test banks)
- ❌ UPI (usually not available in test mode)
- ❌ Wallets (limited in test mode)

### To Test UPI:
1. **Switch to Live Mode**:
   - Get your KYC approved
   - Activate live mode in Razorpay
   - Use live keys: `rzp_live_xxxxx`
   - UPI will be fully functional

2. **OR Test with Cards in Test Mode**:
   - Use test card: `4111 1111 1111 1111`
   - Test the payment flow
   - UPI will work automatically once you go live

## Code Changes Made

I've simplified the Razorpay configuration in `/app/frontend/src/pages/Landing.js` to use default settings. Razorpay automatically shows all enabled payment methods based on your account settings.

### Current Configuration:
```javascript
const options = {
  key: process.env.REACT_APP_RAZORPAY_KEY_ID,
  amount: response.data.amount,
  currency: response.data.currency,
  order_id: response.data.order_id,
  name: 'The Traders Bro',
  description: courseName,
  // Razorpay will show all enabled methods automatically
  theme: {
    color: '#3B82F6'
  }
};
```

## Going Live Checklist

When you're ready to accept real payments:

### 1. Complete KYC in Razorpay
- Submit business documents
- Verify bank account
- Wait for approval (1-2 business days)

### 2. Enable Payment Methods
- Login to Razorpay Dashboard
- Go to Settings → Payment Methods
- Enable: ✅ UPI, ✅ Cards, ✅ Netbanking, ✅ Wallets

### 3. Get Live API Keys
- Go to Settings → API Keys
- Generate **Live Keys** (not test keys)
- Copy `rzp_live_xxxxx` (Key ID)
- Copy the Key Secret

### 4. Update Environment Variables
Replace in `/app/backend/.env`:
```env
RAZORPAY_KEY_ID=rzp_live_YOUR_LIVE_KEY
RAZORPAY_KEY_SECRET=your_live_secret_here
```

Replace in `/app/frontend/.env`:
```env
REACT_APP_RAZORPAY_KEY_ID=rzp_live_YOUR_LIVE_KEY
```

### 5. Test with Real Money
- Make a small test payment (₹10-100)
- Verify UPI shows up
- Complete payment with your UPI app
- Check payment in Razorpay dashboard

### 6. Refund Test Payment
- Go to Razorpay Dashboard → Payments
- Find the test payment
- Click Refund
- Verify refund received

## Expected UPI Options in Live Mode

Once live, users will see:
- 💳 **Pay with UPI ID** - Enter UPI ID manually
- 📱 **UPI Apps** - Google Pay, PhonePe, Paytm, BHIM, etc.
- 📷 **Scan QR Code** - Scan with any UPI app
- ✅ **UPI Intent** - Direct app opening

## Support

If UPI still doesn't show after enabling in dashboard:
1. Check Razorpay Dashboard notifications for pending actions
2. Contact Razorpay Support: support@razorpay.com
3. Chat with Razorpay support in dashboard
4. Check account activation status

## Current Status

✅ **Code is UPI-ready** - No code changes needed
⏳ **Waiting for Razorpay Settings** - Enable UPI in your dashboard
🔄 **Test Mode Active** - UPI will work once you go live

---

**Note**: This is a Razorpay account configuration issue, not a code issue. The payment integration is working correctly.

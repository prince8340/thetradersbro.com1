# Admin Management Guide

## Making Users Admin

### Option 1: Via MongoDB (Direct Database Access)
```bash
mongosh test_database --eval "db.users.updateOne({email: 'user@example.com'}, {\$set: {is_admin: true}})"
```

### Option 2: Via API (Requires existing admin)
```bash
curl -X POST "https://traders-bro.preview.emergentagent.com/api/admin/make-admin/user@example.com" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

## Admin Privileges

Admins can:
- Post ICT Lectures
- All regular user features (post trades, view journal, etc.)

## Current Admin Users

Check current admins:
```bash
mongosh test_database --eval "db.users.find({is_admin: true}, {email: 1, name: 1, _id: 0})"
```

## First User Auto-Admin

The first user to register on the platform automatically becomes an admin.

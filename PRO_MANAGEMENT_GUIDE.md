# PRO Membership Management Guide

## Overview
PRO membership gives users access to:
- Daily Market Views (expert analysis with charts and TradingView links)
- Premium Lectures (exclusive ICT content)

## Requirements
- Only Gmail addresses (@gmail.com) can be granted PRO access
- Admin verification required

## Managing PRO Members

### Add Gmail Address to PRO List
```bash
curl -X POST "https://traders-bro.preview.emergentagent.com/api/admin/allow-pro-email?email=user@gmail.com" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Remove Gmail Address from PRO List
```bash
curl -X DELETE "https://traders-bro.preview.emergentagent.com/api/admin/remove-pro-email/user@gmail.com" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### View All PRO Members
```bash
curl "https://traders-bro.preview.emergentagent.com/api/admin/pro-emails" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

## User Registration
- When a user registers with a Gmail address that's in the PRO list, they automatically get PRO access
- Non-Gmail addresses cannot be PRO members
- Existing users are automatically upgraded when their email is added to PRO list

## PRO Features Access
- Daily Market Views: `/pro/market-views`
- Premium Lectures: `/pro/lectures`

## Current PRO Member
- prouser@gmail.com

## Admin Actions
Only admins can:
- Add/remove emails from PRO list
- Post Daily Market Views
- Post Premium Lectures

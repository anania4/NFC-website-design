# Quick Guide: Update Card Pricing

## 🚀 How to Update Prices (Takes 30 seconds!)

### Step 1: Login to Admin
Go to: `https://your-domain.com/admin/`

### Step 2: Navigate to Card Pricing
Click: **Checkout** → **Card Pricing**

### Step 3: Edit Any Plan
Click on the plan name to edit

### Step 4: Make Changes
Update any field:
- **Price**: Change the amount
- **Name**: Update display name
- **Subtitle**: Modify description
- **Card Range**: Change quantity info
- **Features**: Edit features (one per line)
- **Is Active**: Show/hide on website
- **Display Order**: Change card position

### Step 5: Save
Click **Save** button

### ✅ Done!
The website updates automatically. No cache clearing needed!

---

## 📊 Quick Actions

### Hide a Plan
1. Edit the plan
2. Uncheck **Is active**
3. Save

### Change Card Order
1. In the list view, edit **Display order** column
2. Lower numbers appear first
3. Save

### Add "Popular" Badge
1. Edit the plan
2. Check **Is popular**
3. Save

### Add "Best Value" Badge
1. Edit the plan
2. Check **Is featured**
3. Save

---

## 🔍 Where Changes Appear

✅ Homepage pricing section
✅ Card detail page
✅ Checkout page links

---

## ⚡ Pro Tips

- **Display Order**: Use 10, 20, 30, 40 (easier to reorder later)
- **Features**: Keep them short and clear
- **Price**: System automatically formats with commas
- **Testing**: Open website in incognito to see changes immediately

---

## 🆘 Need Help?

**Changes not showing?**
1. Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
2. Check if plan is marked as "Active"
3. Check logs: `logs/django.log`

**Questions?**
Contact your developer or check `CARD_STATUS_UPDATE_GUIDE.md` for detailed info.

async function issueCoupon() {
    const username = 'logged_in_username'; // Replace with the actual logged in username

    try {
        const response = await fetch('/issue-coupon', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username })
        });
        const result = await response.json();
        const couponResultDiv = document.getElementById('couponResult');
        if (result.success) {
            couponResultDiv.innerHTML = `Coupon Issued: ${result.couponCode}`;
            // Update my coupons list
            loadMyCoupons(username);
        } else {
            couponResultDiv.innerHTML = result.message || 'Error issuing coupon';
        }
    } catch (error) {
        console.error('Error issuing coupon:', error);
    }
}

async function loadMyCoupons(username) {
    try {
        const response = await fetch(`/my-coupons?username=${username}`);
        const coupons = await response.json();
        const myCouponsDiv = document.getElementById('myCoupons');
        myCouponsDiv.innerHTML = '<h3>My Coupons</h3><ul>';
        coupons.forEach(coupon => {
            myCouponsDiv.innerHTML += `<li>${coupon.coupon_code} - ${coupon.description}</li>`;
        });
        myCouponsDiv.innerHTML += '</ul>';
    } catch (error) {
        console.error('Error loading my coupons:', error);
    }
}

// Assume the username is obtained after user logs in
const username = 'logged_in_username'; // Replace with actual logged in username
loadMyCoupons(username);
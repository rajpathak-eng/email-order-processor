# Email Automation for Varifocals and Bifocals Orders

This project automates the process of reading order emails from Shopify and sending follow-up emails to customers who have ordered varifocals or bifocals.

## Project Description

This script connects to your email account, searches for new orders from Shopify, and sends an automatic email to customers who ordered varifocals or bifocals. The follow-up email requests a portrait-style close-up picture to help understand the relevant heights for setting the lenses.

## Features

- Automatically reads emails from a specified sender and subject.
- Identifies orders for varifocals or bifocals.
- Sends a personalized follow-up email to the customer.
- Ensures that duplicate emails are not sent.

## Setup

### Prerequisites

- Python 3.x
- Gmail account with IMAP enabled
- Less secure app access enabled or App Password for Gmail

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/email-automation.git
   cd email-automation

#!/bin/bash
# Created by Almas Adilbek 2014

echo Project name \"without space\": 
read PROJECT_NAME

echo Certificate filename \".cer\":
read CER_FILE

# Convert the .cer file into a .pem file
openssl x509 -in $CER_FILE.cer -inform der -out $PROJECT_NAME"Cert".pem

# Convert the private key’s .p12 file into a .pem file
echo Private key filename \".p12\":
read PKEY_NAME
openssl pkcs12 -nocerts -out $PROJECT_NAME"Key".pem -in $PKEY_NAME.p12

# Finally, combine the certificate and key into a single .pem file
cat $PROJECT_NAME"Cert".pem $PROJECT_NAME"Key".pem > $PROJECT_NAME.pem
echo $PROJECT_NAME.pem file created!

# Remove certificate and private key .pem files
rm -f $PROJECT_NAME"Cert".pem
rm -f $PROJECT_NAME"Key".pem

echo Use $PROJECT_NAME.pem to send push notifications.
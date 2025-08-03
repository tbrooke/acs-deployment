#!/bin/bash

# TrustBlocks Branding Setup Script
# This script ensures all TrustBlocks branding is properly configured

echo "Setting up TrustBlocks branding..."

# Check if branding directory exists
if [ ! -d "branding" ]; then
    echo "Error: branding directory not found!"
    echo "Please ensure you're running this from the docker-compose directory"
    exit 1
fi

# Check if TrustBlocks Logo Library exists
if [ ! -d "../TrustBlocks Logo Library" ]; then
    echo "Warning: TrustBlocks Logo Library directory not found!"
    echo "Expected path: ../TrustBlocks Logo Library"
    echo "Logo images will not be available until this directory is present"
fi

# Verify required logo files exist
LOGO_FILES=(
    "../TrustBlocks Logo Library/Horizontal Version/Color (On Screen)/TrustBlocks Horizontal RGB.png"
    "../TrustBlocks Logo Library/Stacked Version/Color (On Screen)/TrustBlocks Stacked RGB.png"
    "../TrustBlocks Logo Library/Icon/Colour/TrustBlocks Icon Colour.png"
)

for logo in "${LOGO_FILES[@]}"; do
    if [ ! -f "$logo" ]; then
        echo "Warning: Logo file not found: $logo"
    else
        echo "✓ Found: $(basename "$logo")"
    fi
done

# Check branding configuration files
BRANDING_FILES=(
    "branding/share-config-custom.xml"
    "branding/trustblocks-theme.css"
    "branding/messages_en.properties"
)

for file in "${BRANDING_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Error: Required branding file not found: $file"
        exit 1
    else
        echo "✓ Found: $file"
    fi
done

echo ""
echo "TrustBlocks branding setup complete!"
echo ""
echo "To start TrustBlocks Document Management Platform:"
echo "  docker-compose -f community-compose.yaml up -d"
echo ""
echo "Access your platform at:"
echo "  - TrustBlocks Share UI: http://localhost:8080/share"
echo "  - TrustBlocks Content App: http://localhost:8080/content-app"
echo "  - TrustBlocks Admin: http://localhost:8080/control-center"
echo ""
echo "Default login: admin/admin"
#!/bin/bash
set -e  # Quit on error.

VERSION=""

while getopts ":v:" opt; do
    case $opt in
        v)
            VERSION=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            ;;
    esac
done

if [ -z "$VERSION" ]; then
    echo "Error: Version is required. Usage:"
    echo
    echo "  ./generate_release.sh -v vX.X.X"
    echo
    exit 1
fi

echo "Building for version $VERSION"

# Build the webapp.
echo "#############################"
echo " Building the LCM Monitor..."
echo "#############################"
npm install
npm link mbot-js-api
npm run build

# Make a new top level directory and copy everything into it.
INCLUDES="dist/ \
          scripts/deploy_app.sh"
FILE_NAME=mbot_lcm_monitor-$VERSION.tar.gz

mkdir mbot_lcm_monitor-$VERSION
for file in $INCLUDES; do
    cp -r $file mbot_lcm_monitor-$VERSION/
done

# Copy the README.
cp scripts/deploy_readme.txt mbot_lcm_monitor-$VERSION/README.txt

echo
echo "Creating tar file..."
tar -czf $FILE_NAME mbot_lcm_monitor-$VERSION/

rm -rf mkdir mbot_lcm_monitor-$VERSION

echo
echo "Created release: $FILE_NAME"

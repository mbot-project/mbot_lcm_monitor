#!/bin/bash
set -e  # Quit on error.

VERSION=""               # The version of this release.
BRIDGE_VERSION="v1.1.0"  # The MBot Bridge version to download if no path is passed.
BRIDGE_PATH=""           # The path to a local version of MBot Bridge. Overrides downloading a release.

# Directory where the script is executed from
SCRIPT_DIR=$(pwd)

usage() {
  echo "Usage: $0 -v vX.Y.Z [-b PATH/TO/BRIDGE]"
  exit 1
}

while getopts ":v:b:" opt; do
    case $opt in
        v)
            VERSION=$OPTARG
            ;;
        b)
            BRIDGE_PATH=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            usage
            ;;
    esac
done

if [ -z "$VERSION" ]; then
    echo "Error: Version is required."
    usage
    exit 1
fi

echo "Building for version $VERSION"

if [ -n "$BRIDGE_PATH" ]; then
    # Check if the provided path exists
    if [ ! -d "$BRIDGE_PATH/mbot_js" ]; then
        echo "Error: The MBot Bridge JS API does not exist in the provided path: $BRIDGE_PATH"
        usage
        exit 1
    fi
    echo "##############################################################"
    echo "Installing and linking the MBot Bridge from provided path..."
    echo "##############################################################"
    cd $BRIDGE_PATH/mbot_js
    npm install
    npm link
else
    echo "##############################################################"
    echo "Installing and linking the MBot Bridge from release $BRIDGE_VERSION..."
    echo "##############################################################"
    echo "Downloading MBot Bridge $BRIDGE_VERSION"
    wget https://github.com/mbot-project/mbot_bridge/archive/refs/tags/$BRIDGE_VERSION.tar.gz
    tar -xzf $BRIDGE_VERSION.tar.gz
    cd mbot_bridge-${BRIDGE_VERSION#v}/mbot_js
    npm install
    npm link
fi

# Build the webapp.
echo "#############################"
echo " Building the LCM Monitor..."
echo "#############################"
cd $SCRIPT_DIR
npm install
npm link mbot-js-api
npm run build

# Clean up.
if [ -f "$BRIDGE_VERSION.tar.gz" ]; then
    echo
    echo "Cleaning up downloaded files..."
    rm $BRIDGE_VERSION.tar.gz
    rm -rf mbot_bridge-${BRIDGE_VERSION#v}/
fi

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

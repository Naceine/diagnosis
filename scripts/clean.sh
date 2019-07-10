#!/usr/bin/env bash

# Set Message Colors.
reset='\033[0m'      # Text Reset

# Regular Colors.
red='\033[0;31m'     # Red
green='\033[0;32m'   # Green
cyan='\033[0;36m'    # Cyan
#purple='\033[0;35m'  # Purple
yellow='\033[0;33m'  # Yellow
#white='\033[0;37m'  # White

# Bold.
#bred='\033[1;31m'   # Red
#bgreen='\033[1;32m' # Green
# byellow='\033[1;33m' # Yellow
#bwhite='\033[1;37m'  # White
bpurple='\033[1;35m' # Purple

# Underline.
ured='\033[4;31m' # Red

echo -e \
  "${cyan}
  #############################################################################
  # +-----------------------------------------------------------------------+ #
  # |                 Clean Python generated & build files.                 | #
  # +-----------------------------------------------------------------------+ #
  #############################################################################
  Tasks:${reset}
    - [ ] Clean __pycache__ & *.py[co] files.
"

# Sleep for half a second.
sleep .5s

################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Workout the calling directory.
# +--------------------------------------------------------------------------------------------+
################################################################################################
# Run directory: "/scripts/build/*"
PROJECT_DIR="$(cd -P "$(dirname ${BASH_SOURCE[0]})/.." && pwd)"
BUILD_DIR="${PROJECT_DIR}/build"
DIAGNOSIS_DIR="${PROJECT_DIR}/diagnosis"

# Go to the project directory or stop.
cd ${PROJECT_DIR} || exit 1

# Clean .DS_Store files.
find . -type f -name '.DS_Store' -delete

echo -e "${bpurple}Removing __pycache__ & *.py[co] files...${reset}"

# Clean all __pycache__ files.
py_clean() {
  find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
}

py_clean && echo -e "${yellow}
  Tasks:${green}
    - [x] Clean __pycache__ & *.py[co] files.${reset}
"

echo
echo "?Done."

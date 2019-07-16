#!/bin/bash

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
  # |                     Install Project Requirements.                     | #
  # +-----------------------------------------------------------------------+ #
  #############################################################################
  Tasks:${reset}
    - [ ] Install requirements.txt.
    - [ ] Install docproduct.
    - [ ] Download pre-trained models (optional).
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
cd PROJECT_DIR || exit

# Python version cython.sh "3.6" | "3.7"
PY_VERSION="3.6"                  # -v --py-version
PY_EXE="python${PY_VERSION}"      # -e --py-exe
PRE_TRAINED="NO"                  # -p --pre-trained


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | SHOW USAGE MESSAGE.
# +--------------------------------------------------------------------------------------------+
################################################################################################
function usage() {
  echo -e "${b_purple}Description:${purple} Installation script for diagnosis.${reset}"
  echo
  echo -e "${b_white}Usage: ${green}${BASH_SOURCE[0]}${reset}
    -h   | --help            = Show this help message.
    -v   | --py-version      = Which python version to use: <${PY_VERSION}>.
    -e   | --py-executable   = Path to python executable: <${PY_EXE}>.
    -p   | --pre-trained     = Download pretrained models? <${PRE_TRAINED}>
  "
}


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | PARSE PASSED ARGUMENTS.
# +--------------------------------------------------------------------------------------------+
################################################################################################
# Parser loop.
for i in "$@"; do
  case ${i} in
  -h | -H | --help)
    usage
    exit
    ;;
  -v=* | --py-version=*)
    PY_VERSION="${i#*=}"
    PY_EXE="python${PY_VERSION}"
    shift # past argument=value
    ;;
  -e=* | --py-executable=*)
    PY_EXE="${i#*=}"
    shift # past argument=value
    ;;
  -p=* | --pre-trained=*)
    PRE_TRAINED="${i#*=}"
    shift # past argument=value
    ;;
#  --default)
#    DEFAULT=YES
#    shift # past argument with no value
#    ;;
  *)
    # unknown option
    echo -e "${bred}ERROR: ${red}Unknown parameter \"$i\"${reset}"
    usage
    exit 1
    ;;
  esac
done

################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Version of Python to use.
# +--------------------------------------------------------------------------------------------+
################################################################################################

if which ${PY_EXE} >/dev/null 2>&1; then
  echo -e "${b_green}Using Python version: ${PY_VERSION}.${reset}"

elif which python3 >/dev/null 2>&1; then
  PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  echo -e "${b_green}Python version: ${PY_VERSION} detected.${reset}"
  PY_EXE="$(which python3)"

elif which python >/dev/null 2>&1; then
  PY_VERSION=$(python --version 2>&1 | awk '{print $2}')
  echo -e "${b_green}Python version ${PY_VERSION} detected.${reset}"
  PY_EXE="$(which python)"

else
  # Python is not installed
  echo -e "
${red}You don't have any version of Python installed!${reset}
Aborting...
"
  exit 1
fi

# Sleep for half a second.
sleep .5s

# Install requirements.txt
PY_EXE -m pip install -r requirements.txt
echo -e \
  "${cyan}
  #############################################################################
  # +-----------------------------------------------------------------------+ #
  # |                     Install Project Requirements.                     | #
  # +-----------------------------------------------------------------------+ #
  #############################################################################
  Tasks:${green}
    - [x] Install requirements.txt.${reset}
    - [ ] Install gpt2_estimator.
    - [ ] Download pre-trained models (optional).
"

# Sleep for half a second.
sleep .5s

# Install gpt2_estimator
# git clone https://github.com/re-search/DocProduct diagnosis/models/docproduct
# cd diagnosis/models/docproduct
# python setup.py install

echo -e \
  "${cyan}
  #############################################################################
  # +-----------------------------------------------------------------------+ #
  # |                     Install Project Requirements.                     | #
  # +-----------------------------------------------------------------------+ #
  #############################################################################
  Tasks:${green}
    - [x] Install requirements.txt.
    - [x] Install gpt2_estimator.${reset}
    - [ ] Download pre-trained models (optional).
"

# Sleep for half a second.
sleep .5s

wget  https://anaconda.org/pytorch/faiss-cpu/1.2.1/download/linux-64/faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
# To use GPU FAISS use
# wget  https://anaconda.org/pytorch/faiss-gpu/1.2.1/download/linux-64/faiss-gpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
tar xvjf faiss-cpu-1.2.1-py36_cuda9.0.176_1.tar.bz2
pip install mkl

echo
echo "✨Done."
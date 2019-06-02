#!/usr/bin/env bash

# Set Message Colors.
reset='\033[0m'      # Text Reset

# Regular Colors.
red='\033[0;31m'     # Red
green='\033[0;32m'   # Green
cyan='\033[0;36m'    # Cyan
purple='\033[0;35m'  # Purple
#white='\033[0;37m'  # White

# Bold.
bred='\033[1;31m'   # Red
b_purple='\033[1;35m' # Purple
b_green='\033[1;32m'  # Green
b_white='\033[1;37m'  # White

################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Workout the calling directory.
# +--------------------------------------------------------------------------------------------+
################################################################################################

SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SOURCE" ]]; do # resolve $SOURCE until the file is no longer a symlink
  TARGET="$(readlink "$SOURCE")"
  if [[ ${TARGET} == /* ]]; then
    # echo "SOURCE '$SOURCE' is an absolute symlink to '$TARGET'"
    SOURCE="$TARGET"
  else
    DIR="$(dirname "$SOURCE")"
    # echo "SOURCE '$SOURCE' is a relative symlink to '$TARGET' (relative to '$DIR')"
    # if $SOURCE was a relative symlink,
    # we need to resolve it relative to the path where the symlink file was located.
    SOURCE="$DIR/$TARGET"
  fi
done

# Resolved dir & static dir.
RESOLVED_DIR="$(dirname "$SOURCE")"
PROJECT_DIR="$(cd -P ${RESOLVED_DIR}/../ && pwd)"
DIAGNOSI_DIR="${PROJECT_DIR}/diagnosis"
DIAGNOSIS_CORE_DIR="${DIAGNOSI_DIR}/core"

# Go to the project folder or stop.
cd ${PROJECT_DIR} || exit
# Python version cython.sh "3.6" | "3.7"
PY_VERSION="3.7"                  # -v --py-version
PY_EXE="python${PY_VERSION}"      # -e --py-exe
BUILD_LIB="${PROJECT_DIR}"        # -l --build-lib
BUILD_BASE="${PROJECT_DIR}/build" # -b --build-base
BUILD_TEMP="${PROJECT_DIR}/build" # -t --build-temp
CLEAN_BUILD="NO"                  # -c --clean-build
JOBS="4"                          # -j --jobs

################################################################################################
# +--------------------------------------------------------------------------------------------+
# | SHOW USAGE MESSAGE.
# +--------------------------------------------------------------------------------------------+
################################################################################################
function usage() {
  echo -e "${b_purple}Description:${purple} Build script for diagnosis.${reset}"
  echo
  echo -e "${b_white}Usage: ${green}${BASH_SOURCE[0]}${reset}
    -h   | --help            = Show this help message.
    -v   | --py-version      = Which python version to use: <${PY_VERSION}>.
    -e   | --py-executable   = Path to python executable: <${PY_EXE}>.
    -l   | --build-lib       = Path to store Cython build files: <${BUILD_LIB}>.
    -b   | --build-base      = Path to Cython base directory: <${BUILD_BASE}>
    -t   | --build-temp      = Path to Cython temp directory: <${BUILD_TEMP}>
    -c   | --clean-build     = Clean build files before starting build: <${CLEAN_BUILD}>. \"YES\" | \"NO\".
    -j   | --jobs            = No of parallel jobs to run: <${JOBS}>.
  "
  # cmake -h
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
    shift # past argument=value
    ;;
  -e=* | --py-executable=*)
    PY_EXE="${i#*=}"
    shift # past argument=value
    ;;
  -l=* | --build-lib=*)
    BUILD_LIB="${i#*=}"
    shift # past argument=value
    ;;
  -b=* | --build-base=*)
    BUILD_BASE="${i#*=}"
    shift # past argument=value
    ;;
  -c=* | --clean-build=*)
    CLEAN_BUILD="${i#*=}"
    shift # past argument=value
    ;;
  -t=* | --build-temp=*)
    BUILD_TEMP="${i#*=}"
    shift # past argument=value
    ;;
  -j=* | --jobs=*)
    JOBS="${i#*=}"
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

echo -e "${b_purple}${BUILD_LIB}${reset}"
echo -e "${cyan}
################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Building Cython Libraries.
# +--------------------------------------------------------------------------------------------+
################################################################################################
${reset}"


# Clean built folder before building project.
if [[ ${CLEAN_BUILD} == "YES" ]]; then
	sh "${PROJECT_DIR}/scripts/clean.sh"
	echo
fi

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

################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Cython build command.
# +--------------------------------------------------------------------------------------------+
echo -e "${b_white}+ Running...${reset}"
echo -e "${PY_EXE} setup.py build_ext -build-base=${BUILD_BASE} -b${BUILD_LIB} -t${BUILD_TEMP} -j${JOBS}"

${PY_EXE} setup.py build_ext -b${BUILD_LIB} -t${BUILD_TEMP} -j${JOBS}

################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Move generated files.
# +--------------------------------------------------------------------------------------------+
################################################################################################
move() {
  src=$1           # Source folder.
  dest=$2          # Destination folder.
  mkdir -p ${dest} # Create destination folder.

  # Perform find & move.
  mv ${src} ${dest}

  # Display status message.
  echo -e "${b_green}[Moved] ${green}\"${src}\"${b_green} to ${green}\"${dest}\"${reset}"
}

move_with_hierarchy() {
  ext=$1           # Extensions.
  src=$2           # Source folder.
  dest=$3          # Destination folder.

  mkdir -p ${dest} # Create destination folder.

  # Reproduce directory hierarchy.
  rsync -a --prune-empty-dirs --include='*/' --include="*.${ext}" --exclude='*' ${src} ${dest}
  find ${src} -name "*.${ext}" -exec rm -r {} \;

  # Display status message.
  echo -e "${b_green}[Moved] ${green}\"${src}\"${b_green} to ${green}\"${dest}\"${reset}"
}

cd "${DIAGNOSIS_CORE_DIR}" || exit

# Move generated Shared objects & C++ source files to the cython directory.
echo
echo -e "${b_white}Moving generated files...${reset}"

# Move shared objects.
move "${DIAGNOSIS_CORE_DIR}/cython/*.so" "${DIAGNOSIS_CORE_DIR}"
move "${DIAGNOSIS_CORE_DIR}/cython/**/*.so" "${DIAGNOSIS_CORE_DIR}"

# Move generated C++ files.
move_with_hierarchy "cpp" "${DIAGNOSIS_CORE_DIR}/cython" "${BUILD_TEMP}/diagnosis/sources/"


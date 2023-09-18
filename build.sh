# shellcheck disable=SC2128
cd -- "$(dirname "$BASH_SOURCE")" || exit
python3 setup.py py2app
clear
echo "Finished"

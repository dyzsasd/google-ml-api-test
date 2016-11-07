ROOT="$(greadlink -m "$0/../..")"

if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]
  then
    export GOOGLE_APPLICATION_CREDENTIALS=$ROOT/config/google-auth.json
fi

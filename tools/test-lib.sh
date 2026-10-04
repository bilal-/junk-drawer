# Shared by the tests in tools/; each sources it from the checkout's root.

# A throwaway folder in $work, removed on exit. A fixed template, so an odd
# TMPDIR cannot put it anywhere else.
scratch() {
  work=$(mktemp -d "/tmp/junk-drawer-$1.XXXXXX")
  trap 'rm -rf "$work"' EXIT INT TERM
}

# Run from the pre-commit hook, git points these at the commit in progress;
# a test's own repositories must not touch it.
isolate_git() {
  unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_COMMON_DIR \
    GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_PREFIX GIT_NAMESPACE
}

gsutil -m rsync -rdx '\..*|.*/\.[^/]*$|.*/\..*/.*$|_.*' \
	dist/ gs://bdbapi.semitics-archive.org/
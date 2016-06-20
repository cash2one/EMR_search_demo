ps ux | grep nginx | awk '{print $2}' | xargs kill -9

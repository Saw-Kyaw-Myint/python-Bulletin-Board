# Use official Redis image as base
FROM redis:7

# Set working directory (optional)
WORKDIR /data

# Copy custom redis.conf if you have one
# COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose default Redis port
EXPOSE 6379

# Run Redis server with optional config
# CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
CMD ["redis-server"]

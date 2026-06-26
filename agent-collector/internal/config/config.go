package config

import (
	"os"
	"strconv"
)

type Config struct {
	RedisURL           string
	PostgresDSN        string
	CollectionInterval int
	LogLevel           string
}

func Load() *Config {
	interval := 60
	if v := os.Getenv("COLLECTION_INTERVAL"); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			interval = n
		}
	}
	return &Config{
		RedisURL:           getEnv("REDIS_URL", "redis://localhost:6379/1"),
		PostgresDSN:        getEnv("POSTGRES_DSN", "postgres://localhost/foresight"),
		CollectionInterval: interval,
		LogLevel:           getEnv("LOG_LEVEL", "info"),
	}
}
func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

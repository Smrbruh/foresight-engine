package main
import (
	"context"
	"os"
	"os/signal"
	"syscall"
	"github.com/foresight-engine/agent-collector/internal/collector"
	"github.com/foresight-engine/agent-collector/internal/config"
	"github.com/foresight-engine/agent-collector/internal/publisher"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)
func main() {
	cfg := config.Load()
	level, _ := zerolog.ParseLevel(cfg.LogLevel)
	zerolog.SetGlobalLevel(level)
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})
	pub, err := publisher.New(cfg.RedisURL)
	if err != nil {
		log.Fatal().Err(err).Msg("failed to create publisher")
	}
	defer pub.Close()
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
	metricsCh := make(chan collector.Metric, 256)
	col := collector.New(cfg.CollectionInterval)
	go col.Run(ctx, metricsCh)
	go pub.Run(ctx, metricsCh)
	log.Info().Int("interval", cfg.CollectionInterval).Msg("agent-collector started")
	<-sigCh
	log.Info().Msg("shutting down")
	cancel()
}

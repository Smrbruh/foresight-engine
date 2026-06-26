package publisher
import (
	"context"
	"encoding/json"
	"github.com/foresight-engine/agent-collector/internal/collector"
	"github.com/go-redis/redis/v8"
	"github.com/rs/zerolog/log"
)
const metricsChannel = "foresight:metrics"
type Publisher struct {
	client *redis.Client
}
func New(redisURL string) (*Publisher, error) {
	opts, err := redis.ParseURL(redisURL)
	if err != nil {
		return nil, err
	}
	client := redis.NewClient(opts)
	return &Publisher{client: client}, nil
}
func (p *Publisher) Run(ctx context.Context, in <-chan collector.Metric) {
	for {
		select {
		case <-ctx.Done():
			return
		case metric, ok := <-in:
			if !ok {
				return
			}
			p.publish(ctx, metric)
		}
	}
}
func (p *Publisher) publish(ctx context.Context, metric collector.Metric) {
	data, err := json.Marshal(metric)
	if err != nil {
		log.Error().Err(err).Msg("failed to marshal metric")
		return
	}
	if err := p.client.Publish(ctx, metricsChannel, data).Err(); err != nil {
		log.Error().Err(err).Msg("failed to publish metric")
		return
	}
	log.Debug().Str("type", metric.Type).Float64("value", metric.Value).Msg("published metric")
}
func (p *Publisher) Close() error {
	return p.client.Close()
}

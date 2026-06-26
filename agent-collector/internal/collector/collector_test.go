package collector
import (
	"context"
	"testing"
	"time"
)
func TestCollectorCollect(t *testing.T) {
	c := New(1)
	metrics := c.collect()
	if len(metrics) == 0 {
		t.Error("expected non-empty metrics")
	}
	for _, m := range metrics {
		if m.Type == "" {
			t.Error("metric type should not be empty")
		}
		if m.Timestamp.IsZero() {
			t.Error("metric timestamp should not be zero")
		}
	}
}
func TestCollectorRun(t *testing.T) {
	c := New(1)
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	out := make(chan Metric, 100)
	go c.Run(ctx, out)
	<-ctx.Done()
	if len(out) == 0 {
		t.Error("expected at least one metric to be collected")
	}
}

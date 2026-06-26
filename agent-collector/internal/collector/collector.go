package collector
import (
	"context"
	"time"
	"github.com/rs/zerolog/log"
	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/mem"
	"github.com/shirou/gopsutil/v3/net"
)
type Metric struct {
	Type      string            `json:"type"`
	Value     float64           `json:"value"`
	Timestamp time.Time         `json:"timestamp"`
	Labels    map[string]string `json:"labels"`
}
type Collector struct {
	interval time.Duration
}
func New(intervalSeconds int) *Collector {
	return &Collector{interval: time.Duration(intervalSeconds) * time.Second}
}
func (c *Collector) Run(ctx context.Context, out chan<- Metric) {
	ticker := time.NewTicker(c.interval)
	defer ticker.Stop()
	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			metrics := c.collect()
			for _, m := range metrics {
				out <- m
			}
		}
	}
}
func (c *Collector) collect() []Metric {
	var metrics []Metric
	now := time.Now().UTC()
	if percents, err := cpu.Percent(0, false); err == nil && len(percents) > 0 {
		metrics = append(metrics, Metric{Type: "cpu_percent", Value: percents[0], Timestamp: now, Labels: map[string]string{"host": "local"}})
	}
	if vmStat, err := mem.VirtualMemory(); err == nil {
		metrics = append(metrics, Metric{Type: "memory_percent", Value: vmStat.UsedPercent, Timestamp: now, Labels: map[string]string{"host": "local"}})
		metrics = append(metrics, Metric{Type: "memory_bytes_used", Value: float64(vmStat.Used), Timestamp: now, Labels: map[string]string{"host": "local"}})
	}
	if diskStat, err := disk.Usage("/"); err == nil {
		metrics = append(metrics, Metric{Type: "disk_percent", Value: diskStat.UsedPercent, Timestamp: now, Labels: map[string]string{"host": "local", "mount": "/"}})
	}
	if netStats, err := net.IOCounters(false); err == nil && len(netStats) > 0 {
		metrics = append(metrics, Metric{Type: "net_bytes_sent", Value: float64(netStats[0].BytesSent), Timestamp: now, Labels: map[string]string{"host": "local"}})
		metrics = append(metrics, Metric{Type: "net_bytes_recv", Value: float64(netStats[0].BytesRecv), Timestamp: now, Labels: map[string]string{"host": "local"}})
	}
	log.Debug().Int("count", len(metrics)).Msg("collected metrics")
	return metrics
}

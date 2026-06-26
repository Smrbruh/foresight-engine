FROM golang:1.23-alpine AS builder
WORKDIR /app
RUN apk add --no-cache git
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o agent-collector ./cmd/collector
FROM alpine:3.20
RUN apk add --no-cache ca-certificates tzdata
RUN adduser -D -g '' appuser
WORKDIR /app
COPY --from=builder /app/agent-collector .
RUN mkdir -p /var/log/agent-collector && chown appuser:appuser /var/log/agent-collector
USER appuser
CMD ["./agent-collector"]

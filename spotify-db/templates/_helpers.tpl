{{/*
Common labels
*/}}
{{- define "spotify-app.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
MongoDB service name
*/}}
{{- define "spotify-app.mongodbService" -}}
{{- printf "%s-db" .Release.Name }}
{{- end }}
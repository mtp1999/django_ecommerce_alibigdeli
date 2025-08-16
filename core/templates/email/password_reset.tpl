{% extends "mail_templated/base.tpl" %}

{% block subject %}
    reset password
{% endblock %}

{% block html %}
click<a href="{{ reset_url }}" target="_blank">here</a> to reset password
{% endblock %}

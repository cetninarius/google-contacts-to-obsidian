{% for org in repo.organizations %}
{{org.title}}, {{org.name}}
{% endfor %}
{% for org in repo.organizations %}
#{{org.name|replace(" ", "_")}}
{% endfor %}

----
## Contact Info 

{% if repo.birthdays %}
Birthday: {{repo.birthdays.0.date.day}}.{{repo.birthdays.0.date.month}}.
{% endif %}
{% if repo.emailAddresses %}
Emails:
{% for email in repo.emailAddresses %}
    {% if email.type %} {{email.type}} | {% endif %}{{email.value}}
{% endfor %}
{% endif %}
{% if repo.phoneNumbers %}
Phones:
{% for phone in repo.phoneNumbers %}
    {% if phone.type %} {{phone.type}} | {% endif %}{{phone.value}}
{% endfor %}
{% endif %}
{% if repo.addresses %}
Adresses:
{% for address in repo.addresses %}
    {% if address.type %} {{address.type}} | {% endif %}{{ address.formattedValue | replace("\n",", ")}}
{% endfor %}
{% endif %}

{% if repo.events %}
---- 
## Important dates
{% for date in repo.events %}
    {{date.type}} - {{date.date.day}}.{{date.date.month}}.
{% endfor %}
{% endif %}

{% if repo.relations %}
---- 
## Connections
{% for person in repo.relations %}
{{person.type}} | [[{{person.person}}]]
{% endfor %}
{% endif %}

{% if repo.biographies %}
---- 
## Notes
{% for note in repo.biographies %}
{{note.value}}
{% endfor %}
{% endif %}

/*
 *  Copyright 2023 decodable Inc.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

{% macro stop_pipelines(pipelines=none) -%}
  {% for key, value in graph['nodes'].items() %}
    {% set relation = api.Relation.create(database=value['database'], schema=value['schema'], identifier=value['alias']) -%}
    {% set resource_type = value['resource_type'] %}
    {% set is_materialized_test = adapter.should_materialize_tests() and resource_type == 'test' %}
    {% set has_associated_pipe = resource_type == 'model' or is_materialized_test %}
    {% set should_include = pipelines is none or relation.render() in pipelines %}

    {% if has_associated_pipe and should_include %}
      {% set cached_relation = load_cached_relation(relation) %}
      {% if cached_relation is not none %}
        {% do adapter.stop_pipeline(cached_relation) %}
      {% endif %}
    {% endif %}
  {% endfor %}
{%- endmacro %}

{% macro delete_pipelines(pipelines=none) -%}
  {% for key, value in graph['nodes'].items() %}
    {% set relation = api.Relation.create(database=value['database'], schema=value['schema'], identifier=value['alias']) -%}
    {% set resource_type = value['resource_type'] %}
    {% set is_materialized_test = adapter.should_materialize_tests() and resource_type == 'test' %}
    {% set has_associated_pipe = resource_type == 'model' or is_materialized_test %}
    {% set should_include = pipelines is none or relation.render() in pipelines %}

    {% if has_associated_pipe and should_include %}
      {% set cached_relation = load_cached_relation(relation) %}
      {% if cached_relation is not none %}
        {% do adapter.delete_pipeline(cached_relation) %}
      {% endif %}
    {% endif %}
  {% endfor %}
{%- endmacro %}

{% macro delete_streams(streams=none, skip_errors=true) -%}
  {% for key, value in graph['nodes'].items() %}
    {% set relation = api.Relation.create(database=value['database'], schema=value['schema'], identifier=value['alias']) -%}
    {% set resource_type = value['resource_type'] %}
    {% set is_materialized_test = adapter.should_materialize_tests() and resource_type == 'test' %}
    {% set has_associated_stream = resource_type == 'model' or resource_type == 'seed' or is_materialized_test %}
    {% set should_include = streams is none or relation.render() in streams %}

    {% if has_associated_stream and should_include %}
      {% set cached_relation = load_cached_relation(relation) %}
      {% if cached_relation is not none %}
        {% do adapter.delete_stream(cached_relation, skip_errors) %}
      {% endif %}
    {% endif %}
  {% endfor %}
{%- endmacro %}

{% macro cleanup(list=none, seeds=true, models=true, tests=true) -%}
  {% for key, value in graph['nodes'].items() %}
    {% set relation = api.Relation.create(database=value['database'], schema=value['schema'], identifier=value['alias']) -%}
    {% set resource_type = value['resource_type'] %}
    {% set is_materialized_test = adapter.should_materialize_tests() and resource_type == 'test' %}
    {% set passes_filter = list is none or relation.render() in list %}

    {% if passes_filter %}
      {% set cached_relation = load_cached_relation(relation) %}
      {% if cached_relation is not none %}
        {% if resource_type == 'model' and models == true %}
          {% do adapter.drop_relation(cached_relation) %}
        {% elif resource_type == 'seed' and seeds == true %}
          {% do adapter.delete_connection(cached_relation) %}
          {% do adapter.delete_stream(cached_relation) %}
        {% elif is_materialized_test and tests == true %}
          {% do adapter.delete_pipeline(cached_relation) %}
          {% do adapter.delete_stream(cached_relation) %}
        {% endif %}
      {% endif %}
    {% endif %}
  {% endfor %}
{%- endmacro %}

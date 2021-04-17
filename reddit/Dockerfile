FROM ruby:2.5-alpine

RUN apk --no-cache --update add build-base

WORKDIR /app
ADD Gemfile* .

RUN bundle update --bundler && \
    bundle install && \
    apk del build-base

ADD . .

EXPOSE 9292
ENV DATABASE_URL mongo:27017

CMD ["puma"]

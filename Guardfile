# Standard stuff...
guard 'livereload' do
    watch(%r{assets/generated/.+\.(css|js)$})
    watch(%r{assets/images/.+\.(png|gif|jpg)})
    watch(%r{templates/.+\.(jinja|jinja2)})
end

guard 'coffeescript', :input => 'src/coffee', :output => 'src/githubstats/static/js' do
    watch(%r{^src/coffee/.+\.coffee$})
end

guard 'compass' do
  watch(%r{^.+\.sass$})
end

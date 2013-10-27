# Standard stuff...
guard 'livereload' do
    watch(%r{assets/generated/.+\.(css|js)$})
    watch(%r{assets/images/.+\.(png|gif|jpg)})
    watch(%r{templates/.+\.(jinja|jinja2)})
end

guard 'coffeescript', :input => 'coffee', :output => 'static/js' do
    watch(%r{^coffee/.+\.coffee$})
end

guard :shell do
    watch(%r{^scss/.+\.scss$}) do
        `compass compile --force --css-dir="static/css" --sass-dir="scss" --images-dir="static/img" -s compressed`
        puts "Recompiled sass"
    end
end

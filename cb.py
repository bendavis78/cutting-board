#!/usr/bin/env python
from flask import Flask, Response, render_template, make_response
from jinja2 import TemplateNotFound
app = Flask(__name__)

app.config['STATIC_URL'] = '/static/'
app.config['GA_ACCT_ID'] = 'UA-XXXXX-X'

@app.route("/")
@app.route("/<name>")
def render(name='index'):
    try:
        return render_template('{}.html'.format(name), **app.config)
    except TemplateNotFound:
        try:
            not_found_page = render_template('404.html', **app.config)
            return make_response(not_found_page, 404)
        except TemplateNotFound:
            return Response(status=404)

if __name__ == "__main__":
    import sys, os, argparse, shutil
    parser = argparse.ArgumentParser()
    parser.add_argument('bind_to', nargs='?', help='IP:port to bind to', default='localhost:8000')
    parser.add_argument('-b', '--build', help='Build HTML for the given paths', 
                        dest='path', action='store', nargs='+')
    parser.add_argument('-o', '--output', help='Output directory for built html files', default='html', dest='out_dir')
    parser.add_argument('-z', '--zip', help='Create a zip file of the output directory', dest='zip', action='store_true')
    args = parser.parse_args()
    
    ip, port = args.bind_to, 8000
    if ':' in args.bind_to:
        ip, port = args.bind_to.split(':')

    if args.path:
        for path in args.path:
            try:
                app.jinja_env.get_template('%s.html' % path)
            except TemplateNotFound:
                print 'Template not found: "%s.html"' % path
                sys.exit(1)
        if not os.path.exists(args.out_dir):
            os.mkdir(args.out_dir)
        app.config['STATIC_URL'] = 'static/'
        for path in args.path:
            tpl = app.jinja_env.get_template('%s.html' % path)
            rendered = tpl.render(**app.config)
            name = os.path.basename(path)
            file = open(os.path.join(args.out_dir, '%s.html' % name), 'w')
            file.write(rendered.encode('utf-8'))
            file.close()

        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        static_out = os.path.join(args.out_dir, 'static')
        if os.path.exists(static_out):
            shutil.rmtree(static_out)
        shutil.copytree(static_dir, static_out)

        if args.zip:
            root_dir = args.out_dir
            base_dir = os.path.realpath(os.path.join(args.out_dir, '..'))
            shutil.make_archive(args.out_dir, 'zip', args.out_dir, args.out_dir)

    else:
        app.run(debug=True, host=ip, port=int(port))

# -*- coding: utf-8 -*- 
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import logging
import os
#import deleteFile

def index():
    import uuid
    session.uuid = str(uuid.uuid1())
    logger.debug('\n\n------- New UUID : ' + session.uuid)
    return dict()

def upload():
    for r in request.vars:
        if r=="qqfile":
            filename=request.vars.qqfile
            logger.debug('New file uploading : ' + filename)
            db.upload.insert(file=db.upload.file.store(request.body,filename),
                             name=filename,
                             ns=session.uuid)
            return response.json({'success':'false'})

def factor():
    import uuid
    logger.info('New refactoring in progress from ' + request.env.remote_addr)
    query = (db.upload.ns==session.uuid)
    rows = db(query).select()
    file_path = []
    file_raw = []
    f_uuid = str(uuid.uuid1())
    file_dest = os.path.join(request.folder, 'static/rendered', 'rendered-' + f_uuid + '.png')
    # put name file in session
    session.file_dest = os.path.join('/', request.application, 'static/rendered', 'rendered-' + f_uuid + '.png')
    # creating list file
    for tmp in rows:
        file_path.append(os.path.join(request.folder, 'uploads', tmp['file']))
        file_raw.append(tmp['name'])
        logger.debug('File usage : ' + os.path.join(request.folder, 'uploads', tmp['file']))
    # MAIN SOFT
    logger.debug('Importing concateImages')
    concateImage = local_import('concateImage', reload=True)
    try:
        session.data_img, session.data_preview = concateImage.concate_image(file_dest, file_path, file_raw, logger)
    except IOError:
        # Error handling
        logger.error('Wrong file type')
        db(query).delete()
        return response.json({'success':'true', 'processing' : 'failed'})
    # delete all files with session uuid
    logger.debug('Deleting tmp files')
    db(query).delete()
    return response.json({'success':'true', 'processing' : 'done','redirect' : '/' + request.application + '/default/' + 'processed'})

def processed():
    preview = session.file_dest.replace('.png', '-thumb.png')
    css_tag = session.data_img[0]
    html = session.data_preview.split('/')[-3:]
    html_preview = os.path.join('/', request.application, html[0], html[1], html[2])
#    print html_preview
    return dict(url=session.file_dest, preview=preview, data=session.data_img[1:], css_tag=css_tag, html=html_preview)

def user():
    return dict(form=auth())

#def download():
    

def _download():
    import gluon.contenttype
    response.headers['Content-Type']=gluon.contenttype.contenttype('.png')
    return response.stream(open(session.file_dest, 'rb'))

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    print "MUAHAHHAHAHHA"
    return service()



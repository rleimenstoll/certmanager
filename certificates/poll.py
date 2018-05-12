from datetime import datetime
import logging
import ssl

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

from .models import Endpoint, Certificate, CertificateAssociation

logger = logging.getLogger(__name__)


def poll(endpoint):
    """
    Entrypoint to polling mechanism. Will start a scrape of the endpoint's
    certificate.

    Paramaters:
    endpoint -- id of endpoint

    """

    try:
        endpoint = Endpoint.objects.get(pk=endpoint)
    except Endpoint.DoesNotExist:
        logger.error('Endpoint with ID: %s does not exist.' % endpoint)
        # TODO: Propogate errors somewhere, better.
        return

    # Attempt to fetch certificate
    try:
        raw_cert = ssl.get_server_certificate((endpoint.host, endpoint.port), ssl_version=ssl.PROTOCOL_SSLv23)
        logger.debug('Fetched certificate from %s:%s: %s'
                     % (endpoint.host, endpoint.port, raw_cert))
    except Exception as e:  # TODO: More selectively catch exceptions
        logger.error('Failed to fetch certificate from %s:%s: %s'
                     % (endpoint.host, endpoint.port, e))
        return

    # Fetch existing certificate (if there is one)
    existing = \
        endpoint.certificates.order_by('certificateassociation__last_seen')
    if existing.count() > 0:
        curr_cert = existing[0]
        # TODO: Refine comparison
        if raw_cert.strip() == curr_cert:
            logger.info('No certificate change for endpoint %s.' % endpoint)
            return
        else:
            logger.info('Certificate has changed for endpoint %s.' % endpoint)

    # Attempt to parse certificate
    cert = load_pem_x509_certificate(str(raw_cert), default_backend())

    # Get desired aattributes
    not_before = cert.not_valid_before
    not_after = cert.not_valid_after

    # Create new cert
    cert_obj = \
        Certificate(body=raw_cert, not_before=not_before, not_after=not_after)
    cert_obj.save()

    # Create new Cert/Endpoint Association
    assoc_obj = \
        CertificateAssociation(
            endpoint=endpoint,
            certificate=cert_obj,
            last_seen=datetime.now())
    assoc_obj.save()
    logger.info('Created new cert/association %s' % assoc_obj)

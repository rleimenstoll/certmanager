import logging
import ssl

from cryptography.x509 import load_pem_x509_certificate

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
        endpoint = Endpoint.objects.get(id=endpoint)
    except Endpoint.DoesNotExist:
        logger.error('Endpoint with ID: %s does not exist.' % endpoint)
        # TODO: Propogate errors somewhere, better.
        return

    # Attempt to fetch certificate
    try:
        raw_cert = ssl.get_server_certificate((endpoint.host, endpoint.port))
        logger.debug('Fetched certificate from %s:%s: %s'
                     % (endpoint.host, endpoint.port, raw_cert))
    except Exception as e:  # TODO: More selectively catch exceptions
        logger.error('Failed to fetch certificate from %s:%s: %s'
                     % (endpoint.host, endpoint.port, e))
        return

    # Fetch existing certificate (if there is one)
    existing = \
        endpoint.certificate.order_by('certificate_association__last_seen')
    update = False
    if existing.count() > 0:
        curr_cert = existing[0]
        # TODO: Refine comparison
        if raw_cert.strip() == curr_cert:
            logger.info('No certificate change for endpoint %s.' % endpoint)
            return
        else:
            update = True
            logger.info('Certificate has changed for endpoint %s.' % endpoint)

    # Attempt to parse certificate
    cert = load_pem_x509_certificate(raw_cert)

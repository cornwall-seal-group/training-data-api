import config
import azure.common
from azure.storage import CloudStorageAccount
from azure.storage.blob import BlockBlobService, PublicAccess
from azure.storage.blob.models import ContentSettings

account_name = config.STORAGE_ACCOUNT_NAME
account_key = config.STORAGE_ACCOUNT_KEY

# block_blob_service = BlockBlobService(account_name = account_name, account_key = account_key)
# image_metadata = {'id': container_name, 'training': is_training_image, 'test': !is_training_image}


def uploadImageToBlob(block_blob_service, container_name, local_file_name, full_path_to_file, image_metadata):

    if block_blob_service.exists(container_name) == False:
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(
            container_name, public_access=PublicAccess.Container)

    block_blob_service.create_blob_from_path(
        container_name, local_file_name, full_path_to_file, content_settings=ContentSettings(
            content_type='application/png'),
        metadata=image_metadata)

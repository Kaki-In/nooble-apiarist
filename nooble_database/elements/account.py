import database as _database
import local_utils.images as _local_utils_images
import database_layering.facades as _database_layering_facades

class NoobleAccount(_database_layering_facades.DatabaseElementFacade[int]):
    def exists(self) -> bool:
        return self.get_element().exists()
    
    def get_id(self) -> int:
        return self.get_element().get_configuration().get_id()
    
    def get_name(self) -> str:
        return self.get_element().get("name")[0]
    
    def get_surname(self) -> str:
        return self.get_element().get("surname")[0]
    
    def get_password(self) -> str:
        return self.get_element().get("password")[0]
    
    async def get_image(self) -> _local_utils_images.Image:
        image_content = self.get_element().get("image")[0]
        return await _local_utils_images.from_bytes(image_content)
    
    def get_mail(self) -> str:
        return self.get_element().get("mail")[0]
    
    def get_description(self) -> str:
        return self.get_element().get("description")[0]
    
    def is_admin(self) -> bool:
        return self.get_element().get("is-admin")[0] == '1'
    
    def is_verified(self) -> bool:
        return self.get_element().get("is-verified")[0] == '1'
    
    def set_password(self, password:str) -> None:
        self.get_element().set(
            password = _database.SQLString(password)
        )

    def set_image(self, image: _local_utils_images.Image) -> None:
        self.get_element().set(
            image = _database.SQLBlob(bytes(image))
        )

    def set_mail(self, mail:str) -> None:
        self.get_element().set(
            mail = _database.SQLString(mail)
        )

    def set_description(self, description:str) -> None:
        self.get_element().set(
            description = _database.SQLString(description)
        )
    
        
 

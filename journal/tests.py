from django.test import TestCase
import datetime
from django.utils import timezone
from .models import *


class AccessTests(TestCase):
    def setUp(self):
        owner = Owner.objects.create(
            username="testuser",
            email="test@test.pl",
            password="testpassword",
            phone_tel="587741254",
            telegram_chat_id="12122",
        )

        car = Car.objects.create(
            manufacturer="Opel",
            pic="test_pic",
            reg_no="grt7854",
            model="Ampera",
            prod_year="1843",
            engine_model="k24",
            VIN="5426426246423643",
            first_registration=datetime.now(),
            color="f4f4 ; #fr4f",
            fuel="gasoline",
            power=104,
            torque=112,
            engine_capacity=1500
        )
        car.owner.add(owner)

        template = ActionTemplate.objects.create(
            car=car,
            periodic=True,
            important=True,
            #action_popular = models.ForeignKey(ActionPopular, on_delete=models.CASCADE, blank=True, null=True)
            title="Wymina oleju",
            desc="jak wyżej",
            action_milage_period=10000,
            action_days_period=365,
            action_end_date=datetime.now(),
            product="Castrol",
            product_quantity="4L"
        )
        milage = Milage.objects.create(
            car=car,
            milage=188564,
            date=datetime.now()
        )
        file = File.objects.create(
            name="TestFile",
            desc="testFile",
            car=car,
            date=datetime.now()
        )
        action = Action.objects.create(
            ActionTemplate=template,
            milage=milage,
            date=datetime.now(),
            comment="brak",
            cost=50,
            product="Neste",
            file=file
        )


    def test_sites(self):
        login_not_required = [
            "",
            "notify",
            "login"
        ]
        login_required = [
            "logout",
            "car_list",
            "car/1",
            "milage/1",
            "update_milage/1",
            "plan/1",
            "action/list/1",
            "action/add/1",
            "action_list_by_tmpl/1",
            "file/list/1",
            "file/add/1",
            "tmpl_action/1",
            "tmpl_action_add/1",
            "get_file/1"
        ]

        print("Testing not logged user and login_not_required sites")
        for site in login_not_required:
            print("Testing '{}' site".format(site))
            response = self.client.get('/{}'.format(site), follow=True)
            self.assertEqual(response.status_code, 200)
        print("Testing not logged user and login_required sites")
        for site in login_required:
            print("Testing '{}' site".format(site))
            response = self.client.get('/{}'.format(site), follow=True)
            self.assertEqual(response.status_code, 200)

        self.client.login(username="testuser", password="testpassword")
        print("Testing logged user and login_not_required sites")
        for site in login_not_required:
            print("Testing '{}' site".format(site))
            response = self.client.get('/{}'.format(site), follow=True)
            print(response)
            self.assertEqual(response.status_code, 200)
        print("Testing logged user and login_not_required sites")
        for site in login_required:
            print("Testing '{}' site".format(site))
            response = self.client.get('/{}'.format(site), follow=True)
            self.assertEqual(response.status_code, 200)
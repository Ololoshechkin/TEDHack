//
//  SearchResultsTable.swift
//  TouristChat
//
//  Created by Vadim on 24/09/2017.
//  Copyright © 2017 Vadim. All rights reserved.
//

import Foundation
import UIKit

class SearchResultsTable: UITableViewController {
    
    var users = [ServerApi.User]()

    override func viewDidLoad() {
        super.viewDidLoad()
        super.hideKeyboardWhenTappedAround()
        self.navigationItem.title = "Search results"
    }
    
    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return users.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(
            withIdentifier: "UserCell",
            for: indexPath
        ) as! SearchResultCell
        let user = users[indexPath.row]
        cell.photo.image = user.photo ?? #imageLiteral(resourceName: "parisImage")
        cell.nameSurname.text = user.name + " " + user.secondName
        cell.age.text = "\(user.age) years old"
        cell.sex.text = "\(user.sex)".lowercased()
        return cell
    }
    
    override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let user = users[indexPath.row]
        nextPage(id: "UserInfo", preAction: { page in
            (page as! UserInfoViewController).user = user
        })
    }
}
